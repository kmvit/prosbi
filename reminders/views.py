#!-*-coding:utf-8-*-
import os
from random import choice
from django.contrib.auth.decorators import login_required

from django.http import Http404
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, View
from xhtml2pdf import pisa
from account.models import Account
from proshumolitv.mixins import JsonResponseMixin
from proshumolitv.settings import MEDIA_ROOT, BASE_DIR
from reminders.forms import ReminderForm, ReminderItemForm
from reminders.models import Reminder, ReminderItem, RequestReminderLink


class ReminderListView(ListView):
    model = Reminder
    context_object_name = 'reminders'
    template_name = 'reminders/reminders.html'

    def get_queryset(self):
        self.account = Account.get_account(self.request)
        return super(ReminderListView, self).get_queryset().filter(account=self.account)

    def get_context_data(self, **kwargs):
        context = super(ReminderListView, self).get_context_data(**kwargs)
        context['account'] = self.account
        return context


class ReminderView(DetailView):
    model = Reminder
    context_object_name = 'reminder'
    template_name = 'reminders/reminder.html'

    def get_context_data(self, **kwargs):
        context = super(ReminderView, self).get_context_data(**kwargs)
        context['names_only'] = self.request.GET.get('names_only', False)
        return context

    def dispatch(self, request, *args, **kwargs):
        if super(ReminderView, self).get_object().account != Account.get_account(request):
            raise Http404
        return super(ReminderView, self).dispatch(request, *args, **kwargs)


class AddReminder(CreateView, JsonResponseMixin):
    model = Reminder
    form_class = ReminderForm
    template_name = 'reminders/popup__add_reminder.html'
    context_object_name = 'reminder'

    def get(self, request, *args, **kwargs):
        account = Account.get_account(request)
        form = ReminderForm(initial={'account': account})
        popup = render_to_string(self.template_name, RequestContext(request, {'form': form}))
        return self.json_success_response(popup=popup)

    def form_invalid(self, form):
        return self.json_fail_response(message=u'Ошибка')

    def form_valid(self, form):
        form.save()
        return self.json_success_response(message=u'Помянник добавлен')

    def dispatch(self, request, *args, **kwargs):
        account = Account.get_account(request)
        if account.anonym:
            return self.json_fail_response(message=u'Добавлять помянники могут только зарегистрированные пользователи')
        return super(AddReminder, self).dispatch(request, *args, **kwargs)


class DeleteReminder(DeleteView, JsonResponseMixin):
    model = Reminder
    template_name = 'reminders/popup__delete_reminder.html'
    context_object_name = 'reminder'

    def get(self, request, *args, **kwargs):
        reminder = super(DeleteReminder, self).get_object()
        popup = render_to_string(self.template_name, RequestContext(request, {'reminder': reminder}))
        return self.json_success_response(popup=popup)

    def post(self, request, *args, **kwargs):
        account = Account.get_account(request)
        reminder = super(DeleteReminder, self).get_object()
        if reminder not in account.account_reminders.all():
            return self.json_fail_response(message=u'Вы можете удалять только свой помянник')
        if reminder.permanent:
            return self.json_fail_response(message=u'Вы не можете удалить постоянный помянник')
        if 'delete' in request.POST:
            reminder.active = False
            reminder.save()
            return self.json_success_response(message=u'Помянник удален')
        else:
            return self.json_fail_response(message=u'Отмена удаления')


class EditReminder(UpdateView, JsonResponseMixin):
    model = Reminder
    form_class = ReminderForm
    context_object_name = 'reminder'
    template_name = 'reminders/popup__edit_reminder.html'

    def get(self, request, *args, **kwargs):
        account = Account.get_account(request)
        reminder = super(EditReminder, self).get_object()
        form = ReminderForm(instance=reminder)
        popup = render_to_string(self.template_name, RequestContext(request, {'reminder': reminder, 'form': form}))
        return self.json_success_response(popup=popup)

    def form_invalid(self, form):
        return self.json_fail_response(message=u'Ошибка')

    def form_valid(self, form):
        form.save()
        return self.json_success_response(message=u'Помянник сохранен')


class AddReminderItem(CreateView, JsonResponseMixin):
    model = ReminderItem
    form_class = ReminderItemForm
    template_name = 'reminders/popup__add_reminderitem.html'
    context_object_name = 'reminder_item'

    def get(self, request, *args, **kwargs):
        try:
            reminder = Reminder.objects.get(pk=kwargs['reminder_id'])
        except:
            return self.json_fail_response(message=u'Ошибка')
        form = ReminderItemForm(initial={'reminder': reminder})
        popup = render_to_string(self.template_name, RequestContext(request, {'reminder': reminder, 'form': form}))
        return self.json_success_response(popup=popup)

    def form_invalid(self, form):
        return self.json_fail_response(message=u'Ошибка')

    def form_valid(self, form):
        form.save()
        return self.json_success_response(message=u'Имя добавлено')


class DeleteReminderItem(DeleteView, JsonResponseMixin):
    model = ReminderItem
    template_name = 'reminders/popup__delete_reminderitem.html'
    context_object_name = 'reminder_item'

    def get(self, request, *args, **kwargs):
        reminder_item = super(DeleteReminderItem, self).get_object()
        popup = render_to_string(self.template_name, RequestContext(request, {'reminder_item': reminder_item}))
        return self.json_success_response(popup=popup)

    def post(self, request, *args, **kwargs):
        account = Account.get_account(request)
        reminder_item = super(DeleteReminderItem, self).get_object()
        if reminder_item not in ReminderItem.objects.filter(reminder__in=account.account_reminders.all()):
            return self.json_fail_response(message=u'Вы можете удалять имена только из своего помянника')
        if 'delete' in request.POST:
            reminder_item.active = False
            reminder_item.save()
            return self.json_success_response(message=u'Имя удалено')
        else:
            return self.json_fail_response(message=u'Отмена удаления')


class SetPermanentReminderItem(UpdateView, JsonResponseMixin):
    """Set attribute 'from_request' to False"""
    model = ReminderItem
    template_name = 'reminders/popup__set_permanent_reminderitem.html'
    context_object_name = 'reminder_item'

    def get(self, request, *args, **kwargs):
        reminder_item = super(SetPermanentReminderItem, self).get_object()
        if not reminder_item.from_request:
            return self.json_fail_response(message=u'Это имя уже в закрелено в помяннике')
        popup = render_to_string(self.template_name, RequestContext(request, {'reminder_item': reminder_item}))
        return self.json_success_response(popup=popup)

    def post(self, request, *args, **kwargs):
        account = Account.get_account(request)
        reminder_item = super(SetPermanentReminderItem, self).get_object()
        if reminder_item not in ReminderItem.objects.filter(reminder__in=account.account_reminders.all()):
            return self.json_fail_response(message=u'Вы можете изменять имена только из своего помянника')
        if 'set_permanent' in request.POST:
            reminder_item.from_request = False
            reminder_item.save()
            return self.json_success_response(message=u'Имя закреплено как постоянное')
        else:
            return self.json_fail_response(message=u'Отмена')


def export_PDF(request, reminder_id, template_name='pdf/export_to_church_pdf.html'):

    reminder = get_object_or_404(Reminder, pk=reminder_id)

    to_church = request.GET.get('to_church', None)


    if to_church:
        html = render_to_string(template_name, RequestContext(request, {'reminder': reminder, 'STATIC_ROOT': os.path.join(BASE_DIR, 'static')}))
    else:
        html = render_to_string('pdf/export_pdf.html', RequestContext(request, {'reminder': reminder, 'STATIC_ROOT': os.path.join(BASE_DIR, 'static')}))

    pdf_name = "reminder_{rand}.pdf".format(name=reminder.title, rand=''.join([choice('0123456789') for _ in range(7)]))
    pdf = os.path.join(MEDIA_ROOT, pdf_name)

    def convert_PDF(html, output):
        pdf = open(output, "w+b")
        status = pisa.CreatePDF(html.encode('utf-8'), dest=pdf, encoding='UTF-8')
        pdf.close()
        return pdf, status.err

    file, result = convert_PDF(html, pdf)

    response = HttpResponse(open(pdf).read(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=записка_молебен_{}.pdf'.format(reminder.title.lower().replace(' ', '_').encode('utf-8'))
    return response