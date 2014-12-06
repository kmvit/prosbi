from django.contrib import admin
from names.models import Name


class NameAdmin(admin.ModelAdmin):
    list_display = ('nominative', 'genitive', 'genitive_church', 'moderation', 'active')
    list_editable = ('moderation',)

admin.site.register(Name, NameAdmin)