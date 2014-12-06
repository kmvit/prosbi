from django.contrib import admin
from prays.models import Pray, PrayerBook, PrayerBookItem, PrayCategory
from django_markdown.admin import MarkdownModelAdmin

admin.site.register(Pray, MarkdownModelAdmin)

admin.site.register(PrayCategory)

class PrayerBookItemAdmin(admin.StackedInline):
    model = PrayerBookItem

class PrayerBookAdmin(admin.ModelAdmin):
    model = PrayerBook
    inlines = (PrayerBookItemAdmin,)

admin.site.register(PrayerBook, PrayerBookAdmin)