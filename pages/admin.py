from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin
from pages.models import Page


admin.site.register(Page, MarkdownModelAdmin)