#!-*-coding:utf-8-*-
import json
import os
from random import choice
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, DeleteView
from django.views.generic.edit import FormMixin, ProcessFormView
from xhtml2pdf import pisa
from account.models import Account
from prays.forms import PrayerBookForm, AddPrayerBookItemForm
from prays.models import Pray, PrayerBookItem, PrayerBook, PrayCategory
from proshumolitv.mixins import JsonResponseMixin
from proshumolitv.settings import BASE_DIR, MEDIA_ROOT


class PrayListView(ListView):
    model = Pray
    template_name = 'prays/prays.html'
    context_object_name = 'prays'

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        account = Account.get_account(self.request)
        PrayerBook.create_defaults(account)
        context['account'] = account
        return context


class PrayCategoryListView(ListView):
    model = PrayCategory
    template_name = 'prays/pray_categories.html'
    context_object_name = 'pray_categories'

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        account = Account.get_account(self.request)
        PrayerBook.create_defaults(account)
        context['account'] = account
        return context


class PrayView(DetailView, FormMixin):
    model = Pray
    template_name = 'prays/pray.html'
    context_object_name = 'pray'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        account = Account.get_account(self.request)
        prayerbook = account.prayerbook
        context['account'] = account
        context['pray_in_my_praybook'] = prayerbook.pray_added(super(self.__class__, self).get_object())
        return context


class PrayerBookView(DetailView, ProcessFormView, FormMixin, JsonResponseMixin):
    model = PrayerBook
    template_name = 'prays/prayer_book.html'
    context_object_name = 'prayer_book'
    form_class = AddPrayerBookItemForm

    def get_context_data(self, **kwargs):
        context = super(PrayerBookView, self).get_context_data(**kwargs)
        form = self.get_form(self.get_form_class())
        form.fields['pray'].choices = [('', u'Выберите молитву')] + [(p.id, p.name) for p in Pray.objects.exclude(pk__in=[pray.id for pray in super(PrayerBookView, self).get_object().prays.all()])]
        context['form'] = form
        return context

    def get_initial(self):
        account = Account.get_account(self.request)
        return {'prayerbook': account.prayerbook}

    def form_valid(self, form):
        data = form.cleaned_data
        prayerbook = data['prayerbook']
        pray = data['pray']
        index = prayerbook.prays.count() + 1
        item = PrayerBookItem.objects.create(prayerbook=prayerbook, pray=pray, index=index)
        return self.json_success_response(message=u'Молитва добавлена')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        account = Account.get_account(self.request)
        book, created = PrayerBook.objects.get_or_create(account=account)
        if 'pk' in kwargs and str(book.id) != kwargs['pk']:
            raise Http404
        return super(PrayerBookView, self).dispatch(request, *args, **kwargs)


class SelfPrayerBookView(PrayerBookView):
    def get_object(self, queryset=None):
        account = Account.get_account(self.request)
        book, created = PrayerBook.objects.get_or_create(account=account)
        return book


class DeletePrayerBookItem(DeleteView, JsonResponseMixin):
    model = PrayerBookItem
    template_name = 'prays/popup__delete_prayerbook_item.html'
    context_object_name = 'prayerbook_item'

    def delete(self, request, *args, **kwargs):
        pass

    def get(self, request, *args, **kwargs):
        item = super(self.__class__, self).get_object()
        popup = render_to_string(self.template_name, RequestContext(request, {'prayerbook_item': item}))
        return self.json_success_response(popup=popup)

    def post(self, request, *args, **kwargs):
        account = Account.get_account(request)
        item = super(self.__class__, self).get_object()
        if item not in account.prayerbook.prayerbook_items.all():
            return self.json_fail_response(message=u'Вы можете молитвы только из своего молитвослова')
        if 'delete' in request.POST:
            item.delete()
            return self.json_success_response(message=u'Молитва удалена')
        else:
            return self.json_fail_response(message=u'Отмена удаления')


def move_prayerbook_item(request, item_id):
    if request.method == 'GET':
        account = Account.get_account(request)
        if account:
            prayer_book = account.prayerbook
            item = get_object_or_404(PrayerBookItem, pk=item_id)
            items = prayer_book.prayerbook_items.all()
            if item in items:
                direction = request.GET.get('direction', None)

                if direction == 'up' and item.index > 1:
                    prev_item = items.filter(index=item.index - 1)
                    if prev_item:
                        prev_item = prev_item[0]
                        prev_item.index = item.index
                        prev_item.save()
                        item.index = item.index - 1
                        item.save()
                        return HttpResponse(json.dumps({'status': True, 'message': u'Молитва перемещена вверх'}), 'json')

                elif direction == 'down':
                    next_item = items.filter(index=item.index + 1)
                    if next_item:
                        next_item = next_item[0]
                        next_item.index = item.index
                        next_item.save()
                        item.index = item.index + 1
                        item.save()
                        return HttpResponse(json.dumps({'status': True, 'message': u'Молитва перемещена вниз'}), 'json')

    return HttpResponse(json.dumps({'status': False, 'message': u'Молитва не перемещена'}), 'json')


def add_pray_to_prayerbook(request, pray_id):
    pray = get_object_or_404(Pray, pk=pray_id)
    account = Account.get_account(request)
    prayerbook = account.prayerbook
    item = prayerbook.add_pray(pray)
    if item:
        return HttpResponse(json.dumps({'status': True, 'message': u'Молитва добавлена в молитвослов'}), 'json')

    return HttpResponse(json.dumps({'status': False, 'message': u'Вы уже добавили эту молитву в свой молитвослов'}), 'json')


def export_pray_PDF(request, pray_id, template_name='pdf/export_pray_pdf.html'):

    pray = get_object_or_404(Pray, pk=pray_id)
    html = render_to_string(template_name, RequestContext(request, {'pray': pray, 'STATIC_ROOT': os.path.join(BASE_DIR, 'static')}))

    pdf_name = "pray_{rand}.pdf".format(rand=''.join([choice('0123456789') for _ in range(7)]))
    pdf = os.path.join(MEDIA_ROOT, pdf_name)

    def convert_PDF(html, output):
        pdf = open(output, "w+b")
        status = pisa.CreatePDF(html.encode('utf-8'), dest=pdf, encoding='UTF-8')
        pdf.close()
        return pdf, status.err

    file, result = convert_PDF(html, pdf)

    response = HttpResponse(open(pdf).read(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename={}.pdf'.format(pray.name.lower().replace(' ', '_').encode('utf-8'))
    return response


def export_prayerbook_PDF(request, prayerbook_id, template_name='pdf/export_prayerbook_pdf.html'):

    prayerbook = get_object_or_404(PrayerBook, pk=prayerbook_id)
    html = render_to_string(template_name, RequestContext(request, {'prayerbook': prayerbook, 'STATIC_ROOT': os.path.join(BASE_DIR, 'static')}))

    pdf_name = "prayerbook_{rand}.pdf".format(rand=''.join([choice('0123456789') for _ in range(7)]))
    pdf = os.path.join(MEDIA_ROOT, pdf_name)

    def convert_PDF(html, output):
        pdf = open(output, "w+b")
        status = pisa.CreatePDF(html.encode('utf-8'), dest=pdf, encoding='UTF-8')
        pdf.close()
        return pdf, status.err

    file, result = convert_PDF(html, pdf)

    response = HttpResponse(open(pdf).read(), content_type='application/pdf')
    response['Content-Disposition'] = u'attachment; filename=Молитвослов.pdf'.encode('utf-8')
    return response