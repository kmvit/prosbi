#!-*-coding:utf-8-*-prays/book/1/
from datetime import datetime
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import mail_admins
from django.db.models import Q
from django.forms.models import modelformset_factory
from django.http.request import QueryDict
from django.http.response import HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.views.generic import ListView, CreateView
from django.views.generic.detail import DetailView
from account.models import Account
from names.forms import NameForm
from names.models import Name
from proshumolitv.mixins import JsonResponseMixin
from reminders.models import RequestReminderLink, Reminder, ReminderItem
from requests.forms import RequestForm, PrayEventForm, CommentForm
from requests.models import Request, PrayEvent, Comment
from proshumolitv.settings import REQUESTS_ON_PAGE


class RequestListView(ListView):
    model = Request
    template_name = 'requests/requests.html'
    context_object_name = 'requests'
    paginate_by = REQUESTS_ON_PAGE

    def get_queryset(self):
        return Request.moderated.all()

    def get_context_data(self, **kwargs):
        context = super(RequestListView, self).get_context_data(**kwargs)
        account = Account.get_account(self.request)
        context['account'] = account
        context['form'] = RequestForm(initial={'account': account})
        return context


class RequestView(DetailView):
    model = Request
    template_name = 'requests/request.html'
    context_object_name = 'req'

    def get_context_data(self, **kwargs):
        context = super(RequestView, self).get_context_data(**kwargs)
        account = Account.get_account(self.request)
        context['pray_event_form'] = PrayEventForm(initial={'request': self.object, 'prayer': account})
        context['comment_form'] = CommentForm(initial={'request': self.object, 'account': account})
        context['form'] = RequestForm(initial={'account': account})
        context['account'] = account
        return context


class AddRequest(CreateView, JsonResponseMixin):
    model = Request
    template_name = 'requests/popup__add_request.html'
    context_object_name = 'request'
    form_class = RequestForm
    moderation = False

    def get(self, request, *args, **kwargs):
        account = Account.get_account(request)
        form = RequestForm(initial={'account': account})
        popup = render_to_string(self.template_name, RequestContext(request, {'form': form}))
        return self.json_success_response(popup=popup)

    def get_form_kwargs(self):
        raw_names = self.request.POST.getlist('raw_names')
        names = list(Name.objects.filter(genitive__in=raw_names))
        new_names = []
        for name in raw_names:
            if name not in [n.genitive for n in names]:
                self.moderation = True
                new_name = Name(genitive=name)
                new_name.save()
                new_names.append(new_name)

        kwargs = super(AddRequest, self).get_form_kwargs()
        mutable = kwargs['data']._mutable
        kwargs['data']._mutable = True
        kwargs['data'].update(QueryDict('&'.join(['names=%d' % n.id for n in names+new_names])))
        kwargs['data']._mutable = mutable
        self.new_names = new_names
        return kwargs

    def form_invalid(self, form):
        errors = {field.name: field.errors for field in form if field.errors}
        return self.json_fail_response(message=u'Ошибка при добавлении просьбы', errors=errors)

    def form_valid(self, form):
        req = form.save()
        if self.moderation:
            mail_admins(
                u'Добавлена новая молитвенная просьба. Необходима модерация имен.',
                u'Зарегистрированы новые имена: "{names}". Дата: {date}'.format(names=u', '.join([name.genitive for name in req.names.all()]), date=datetime.now().strftime('%d.%m.%Y'))
            )
            NameFormSet = modelformset_factory(Name, form=NameForm, max_num=4)
            formset = NameFormSet(queryset=req.names.filter(moderation=True))
            html = render_to_string('names/popup__add_names.html', RequestContext(self.request, {'formset': formset, 'request_id': req.id}))
            return self.json_success_response(message=u'Молебная просьба добавлена, но некоторые имена требуют модерации', html=html)

        return self.json_success_response(message=u'Молебная просьба добавлена')


class AddPrayEvent(CreateView, JsonResponseMixin):
    model = PrayEvent
    form_class = PrayEventForm

    def form_invalid(self, form):
        return self.json_fail_response(message=u'Ошибка')

    def form_valid(self, form):
        data = form.cleaned_data
        prayer = data['prayer']
        request = data['request']

        reminder = Reminder.objects.get(account=prayer, type=request.category.type)

        if request.old_names:
            ReminderItem.objects.create(
                reminder=reminder,
                name=request.old_names,
                comment=request.comment,
                category=request.category,
                from_request=True,
            )

        for name in request.names.all():
            ReminderItem.objects.create(
                reminder=reminder,
                name=name.genitive,
                comment=request.comment,
                category=request.category,
                from_request=True,
            )

        if not PrayEvent.objects.filter(prayer=prayer, request=request).exists():
            form.save()
            return self.json_success_response(message=u'Вы помолитесь по этой просьбе')
        else:
            return self.json_fail_response(message=u'Вы уже помолитесь по этой просьбе')


class RequestPrayersList(DetailView, JsonResponseMixin):
    model = Request
    template_name = 'requests/popup__request_prayers_list.html'
    context_object_name = 'req'

    def render_to_response(self, context, **response_kwargs):
        popup = render_to_string(self.template_name, context)
        return self.json_success_response(popup=popup)


class AddComment(CreateView, JsonResponseMixin):
    model = Comment
    form_class = CommentForm

    def form_invalid(self, form):
        return self.json_fail_response(message=u'Ошибка сохранения комментария')

    def form_valid(self, form):
        comment = form.save()
        if not comment.request.account.anonym:
            message = render_to_string('requests/add_comment_email.html', RequestContext(self.request, {'comment': comment}))
            try:
                comment.request.account.user.email_user(u'Добавлен новый комментарий к вашей просьбе', message)
            except:
                pass
        return self.json_success_response(message=u'Комментарий сохранен')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AddComment, self).dispatch(request, *args, **kwargs)
