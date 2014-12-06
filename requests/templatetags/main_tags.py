#!-*-coding:utf-8-*-
from django.contrib.auth.forms import AuthenticationForm
from django.template import Library
from account.models import Account

register = Library()


@register.inclusion_tag('tags/header.html', takes_context=True)
def header_tag(context):
    request = context.get('request', None)
    account = Account.get_account(request)
    page = context['request'].META['PATH_INFO']
    form = AuthenticationForm()
    form.fields['username'].label = u'Email'
    form.fields['password'].label = u'Пароль'

    data = {
        'auth': request.user.is_authenticated if request else False,
        'account': account,
        'page': page,
        'login_form': form,
    }
    return data
