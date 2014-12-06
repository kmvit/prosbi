from django.shortcuts import render
from django.views.generic import DetailView
from pages.models import Page


class PageView(DetailView):
    model = Page
    template_name = 'pages/page.html'
    context_object_name = 'page'
    slug_field = 'url'

    def get_queryset(self):
        return super(PageView, self).get_queryset().filter(active=True)