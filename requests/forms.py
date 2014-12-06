#!-*-coding:utf-8-*-

import re
from django import forms
from django.core.exceptions import ValidationError
from requests.models import Request, PrayEvent, Comment


class RequestForm(forms.ModelForm):

    # live_names = forms.CharField(label=u'Имена', widget=forms.TextInput(attrs={'id': 'live_names_input'}))

    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = None
        self.fields['names'].required = False

    def clean_comment(self):
        data = self.cleaned_data['comment']
        if re.search(r'\d\s*\d', data) or '@' in data or '$' in data:
            raise ValidationError(u'Запрещаются символы: более 2-х идущих подряд цифр (даже если через пробелы), @, $')
        return data

    class Meta:
        model = Request
        exclude = ('old_names', 'old_prayer_count', 'active', 'date')
        widgets = {
            'account': forms.HiddenInput(),
            'names': forms.MultipleHiddenInput(),
        }


class PrayEventForm(forms.ModelForm):
    class Meta:
        model = PrayEvent
        fields = ('request', 'prayer')
        widgets = {
            'request': forms.HiddenInput(),
            'prayer': forms.HiddenInput(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('moderation', 'active')
        widgets = {
            'request': forms.HiddenInput(),
            'account': forms.HiddenInput(),
        }