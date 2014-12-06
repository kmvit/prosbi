#!-*-coding:utf-8-*-

from django import forms
from reminders.models import Reminder, ReminderItem


class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        exclude = ('active', 'permanent', 'requests', 'type')
        widgets = {
            'account': forms.HiddenInput(),
        }


class ReminderItemForm(forms.ModelForm):
    class Meta:
        model = ReminderItem
        exclude = ('date', 'active', 'from_request', 'category')
        widgets = {
            'reminder': forms.HiddenInput(),
        }