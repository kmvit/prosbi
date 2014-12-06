#!-*-coding:utf-8-*-
from django.contrib import admin
from requests.models import Request, Category, PrayEvent, Comment


class RequestAdmin(admin.ModelAdmin):
    model = Request
    filter_horizontal = ('names',)
    list_display = ('get_account', 'category', 'get_names', 'comment', 'active')

    def get_account(self, obj):
        return obj.account.name or u'Аноним'

    def get_names(self, obj):
        if obj.old_names:
            return obj.old_names
        return u', '.join([name.genitive for name in obj.names.all()])

    get_account.short_description = u'Аккаунт'
    get_names.short_description = u'Имена'


admin.site.register(Request, RequestAdmin)
admin.site.register(Category)
admin.site.register(PrayEvent)
admin.site.register(Comment)