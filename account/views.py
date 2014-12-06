#!-*-coding:utf-8-*-
from datetime import datetime
import json
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import mail_admins
from django.forms.models import modelformset_factory, inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from account.forms import AccountForm, RegisterForm, SocialForm
from account.models import Account, Social
from names.models import Name
from names.forms import NameForm


@require_POST
def sign_up(request):
    account = Account.create_raw_account(request)
    if account:
        message = render_to_string('account/signup_email.html', {'account': account})
        account.user.email_user(u'Запрошена реистрация на сайте', message)
        return HttpResponse(json.dumps(
            {'message': u'Для продолжения регистрации перейдтие по ссылке, которая отправлена на указанную почту'}), 'json')
    else:
        return HttpResponse(json.dumps({'message': u'Пользователь с таким адресом уже существует'}), 'json')


def register(request, token):
    if not token:
        return HttpResponseRedirect('/')
    try:
        account = Account.objects.get(token=token, user__is_active=False)
    except Account.DoesNotExist:
        return HttpResponseRedirect('/')
    is_registered = False

    if request.method == 'GET':
        form = RegisterForm(instance=account)
        SocialFormSet = inlineformset_factory(Account, Social, fk_name='account', extra=0)
        return render_to_response('account/registration.html', RequestContext(request, {'form': form, 'social_formset': SocialFormSet(instance=account)}))

    if request.method == 'POST':
        n = request.POST.get('name_register', None)
        if n:
            name, created = Name.objects.get_or_create(genitive=n)

            form = RegisterForm(request.POST, instance=account)
            SocialFormSet = inlineformset_factory(Account, Social, fk_name='account')
            social_formset = SocialFormSet(request.POST, instance=account)
            if form.is_valid() and social_formset.is_valid():
                account = form.save(commit=False)
                account.name = name
                account.anonym = False
                account.save()
                social_formset.save()
                is_registered = True
                if not name.moderation:
                    return HttpResponse(json.dumps({'status': True, 'redirect': '/', 'message': u'Регистрация прошла успешно'}), 'json')
                else:
                    mail_admins(
                        u'Регистрация нового пользователя. Необходима модерация имени.',
                        u'Пользователем {user} зарегистрировано новое имя "{name}". Дата: {date}'.format(name=name.genitive, user=account.user.username, date=datetime.now())
                    )
                    html = render_to_string('names/popup__name_register.html', RequestContext(request, {'form': NameForm(instance=name), 'name': name}))
                    return HttpResponse(json.dumps({'status': True, 'html': html, 'message': u'Ваша учетная запись зарегистрирована, но находится на модерации, пока вы не сможете пользоваться возможностями, доступными зарегистрированнным пользователям'}), 'json')

    return render_to_response('account/registration.html',
                              RequestContext(request, {'form': form, 'social_formset': social_formset, 'is_registered': is_registered}))


@require_POST
def login(request):
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        account = user.account
        if account.moderation:
            return HttpResponse(json.dumps({'status': False, 'message': u'Аккаунт находится на модерации'}), 'json')
        auth.login(request, user)
        return HttpResponse(json.dumps({'status': True, 'message': u'Авторизация успешно пройдена'}), 'json')
    else:
        return HttpResponse(json.dumps({'status': False, 'message': u'Логин или пароль введены неверно'}), 'json')


@login_required()
def logout(request):
    auth.logout(request)
    if request.GET:
        return HttpResponseRedirect(request.GET.get('next'))
    else:
        return HttpResponseRedirect('/')
