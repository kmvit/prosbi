#!-*-coding:utf-8-*-
import json
from django.db.models import Q
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.generic import ListView, View, UpdateView
from django.views.generic.edit import CreateView
from names.forms import NameForm
from names.models import Name
from proshumolitv.mixins import JsonResponseMixin
from requests.models import Request


class LiveSearchNames(ListView, JsonResponseMixin):
    model = Name
    context_object_name = 'names'

    def get_context_data(self, **kwargs):
        context = super(LiveSearchNames, self).get_context_data(**kwargs)
        context['q'] = self.q
        return context

    def get_queryset(self):
        self.q = self.request.GET.get('term', None)
        return super(LiveSearchNames, self).get_queryset().filter(moderation=False).filter(genitive__istartswith=self.q)[:10]

    def render_to_response(self, context, **response_kwargs):
        names = context['names']
        return HttpResponse(json.dumps([{'label': u'{1} ({0})'.format(name.nominative, name.genitive), 'value': name.genitive, 'id': name.id} for name in names]), 'json')


class UpdateName(UpdateView, JsonResponseMixin):
    model = Name
    form_class = NameForm

    def form_invalid(self, form):
        return self.json_fail_response(message=u'Имя не сохранено')

    def form_valid(self, form):
        form.save()
        return self.json_success_response(message=u'Имя сохранено')


def add_names(request, request_id, template_name='names/popup__add_names.html'):
    req = get_object_or_404(Request, pk=request_id)
    NameFormSet = modelformset_factory(Name, form=NameForm, max_num=4)
    if request.method == 'POST':
        formset = NameFormSet(request.POST)
        if formset.is_valid():
            names = formset.save()
            req.names.add(*names)
            req.active = True
            req.save()

            return HttpResponse(json.dumps({'status': True, 'message': u'Имена добавлены'}), 'json')
        else:
            return HttpResponse(json.dumps({'status': False, 'message': u'Ошибка', 'errors': formset.errors}))
    else:
        names = request.GET.getlist('names')[:4]
        NameFormSet = modelformset_factory(Name, form=NameForm, max_num=len(names))
        formset = NameFormSet(initial=[{'genitive': name} for name in names])
        html = render_to_string(template_name, RequestContext(request, {'formset': formset, 'request_id': req.id}))
        return HttpResponse(json.dumps({'status': True, 'html': html}), 'json')