#!-*-coding:utf-8-*-
from django import forms
from names.models import Name


class NameForm(forms.ModelForm):
    class Meta:
        model = Name
        exclude = ('active', 'moderation')


