#!-*-coding:utf-8-*-

from django import forms
from prays.models import PrayerBook, Pray


class AddPrayerBookItemForm(forms.Form):
    prayerbook = forms.ModelChoiceField(queryset=PrayerBook.objects.all(), widget=forms.HiddenInput())
    pray = forms.ModelChoiceField(queryset=Pray.objects.all(), label=u'Молитва', empty_label=u'Выберите молитву')


class PrayerBookForm(forms.ModelForm):
    class Meta:
        model = PrayerBook
        widgets = {
            'prays': forms.CheckboxSelectMultiple(),
            'account': forms.HiddenInput()
        }