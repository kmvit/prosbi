from django.conf.urls import patterns, include, url
from reminders.views import ReminderListView, Reminder, ReminderView, AddReminder, DeleteReminder, EditReminder, DeleteReminderItem, AddReminderItem, SetPermanentReminderItem

urlpatterns = patterns('',
    url(r'^$', ReminderListView.as_view(), name='reminders'),
    url(r'^(?P<pk>\d+)/$', ReminderView.as_view(), name='reminder'),
    url(r'^add/$', AddReminder.as_view(), name='add_reminder'),
    url(r'^edit/(?P<pk>\d+)/$', EditReminder.as_view(), name='edit_reminder'),
    url(r'^delete/(?P<pk>\d+)/$', DeleteReminder.as_view(), name='delete_reminder'),

    url(r'^item/add/(?P<reminder_id>\d+)/$', AddReminderItem.as_view(), name='add_reminderitem'),
    url(r'^item/delete/(?P<pk>\d+)/$', DeleteReminderItem.as_view(), name='delete_reminderitem'),
    url(r'^item/set_permanent/(?P<pk>\d+)/$', SetPermanentReminderItem.as_view(), name='set_permanent_reminderitem'),

    url(r'^export/pdf/(?P<reminder_id>\d+)/$', 'reminders.views.export_PDF', name='export_pdf'),


)