#!-*-coding:utf-8-*-
from datetime import timedelta, datetime
from celery import Celery
from celery.task import task
from celery.task.base import periodic_task
from names.models import Name
from reminders.models import Reminder, ReminderItem

app = Celery('reminders', broker='django://')

@app.task()
def clear_reminder_names():
    reminder_items = ReminderItem.objects.filter(from_request=True)
    for item in reminder_items:
        account = item.reminder.account
        if item.date + timedelta(days=account.days_for_reminder) > datetime.now():
            item.active = False
            item.save()
