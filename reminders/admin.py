from django.contrib import admin
from reminders.models import Reminder, ReminderItem, RequestReminderLink


admin.site.register(Reminder)

class ReminderItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'comment', 'from_request', 'category', 'active')

admin.site.register(ReminderItem, ReminderItemAdmin)
