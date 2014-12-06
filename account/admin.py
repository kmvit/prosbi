from django.contrib import admin
from account.models import Account, Dignity, Confession, Social, SocialNetwork


class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'dignity', 'confession', 'days_for_reminder')

    def get_queryset(self, request):
        return super(AccountAdmin, self).get_queryset(request).filter(anonym=False)

admin.site.register(Account, AccountAdmin)
admin.site.register(Dignity)
admin.site.register(Confession)
admin.site.register(Social)
admin.site.register(SocialNetwork)
