#!-*-coding:utf-8-*-
from django import forms
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from account.models import Account, Social
from reminders.models import Reminder


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = ('active', 'anonym', 'name')
        widgets = {
            'user': forms.HiddenInput(),
            'token': forms.HiddenInput(),
        }


class RegisterForm(AccountForm):
    password = forms.CharField(label=u'Пароль', max_length=100, widget=forms.PasswordInput())
    password_confirm = forms.CharField(label=u'Пароль', max_length=100, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        if cleaned_data['password'] != cleaned_data['password_confirm']:
            raise ValidationError(u'Пароли не совпадают')
        return cleaned_data

    def save(self, commit=True):
        account = super(RegisterForm, self).save()
        account.user.set_password(self.cleaned_data['password'])
        account.user.is_active = True
        account.user.save()
        Reminder.create_defaults(account)

        return super(RegisterForm, self).save(commit=commit)


class SocialForm(forms.ModelForm):
    class Meta:
        model = Social
        widgets = {
            'account': forms.HiddenInput()
        }
