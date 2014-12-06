#!-*-coding:utf-8-*-
from django.db import models
from django.db.models import Count
from proshumolitv.managers import ActiveManager
from reminders.settings import REMINDER_TYPES, FOR_HEALTH_TYPE, FOR_REPOSE_TYPE


class Reminder(models.Model):
    account = models.ForeignKey('account.Account', verbose_name=u'Аккаунт', related_name='account_reminders')
    title = models.CharField(u'Название', max_length=150)

    type = models.PositiveSmallIntegerField(u'Тип', choices=REMINDER_TYPES, default=3)
    requests = models.ManyToManyField('requests.Request', through='RequestReminderLink', related_name='request_reminders')
    permanent = models.BooleanField(u'Постоянный', default=False)

    active = models.BooleanField(u'Активно', default=True)
    objects = ActiveManager()

    def __unicode__(self):
        return self.title

    def get_requests(self):
        return self.requests.filter(active=True)

    @classmethod
    def create_defaults(self, account):
        for_health, created = Reminder.objects.get_or_create(
            account=account,
            title=u'О здравии',
            permanent=True,
            type=FOR_HEALTH_TYPE
        )

        for_repose, created = Reminder.objects.get_or_create(
            account=account,
            title=u'Об упокоении',
            permanent=True,
            type=FOR_REPOSE_TYPE
        )

        return for_health, for_repose

    def get_requests_count(self):
        return self.reminder_requests.count()

    def get_names_count(self):
        return self.reminder_requests.aggregate(Count('request__names'))['request__names__count']

    def get_items_count(self):
        return self.reminder_items.all().count()

    class Meta:
        ordering = ['-permanent', 'title']
        verbose_name = u'Помянник'
        verbose_name_plural = u'Помянники'


class ReminderItem(models.Model):
    reminder = models.ForeignKey(Reminder, verbose_name=u'Помянник', related_name='reminder_items')
    name = models.CharField(u'Имя (в род.падеже)', max_length=150)
    comment = models.TextField(u'Комментарий', blank=True)
    date = models.DateTimeField(auto_now_add=True)

    from_request = models.BooleanField(u'Из молитвенной просьбы', default=False)
    category = models.ForeignKey('requests.Category', verbose_name=u'Категория', null=True, blank=True)

    active = models.BooleanField(default=True)
    objects = ActiveManager()

    def __unicode__(self):
        return str(self.id)

    class Meta:
        ordering = ['date']
        verbose_name = u'Запись в помяннике'
        verbose_name_plural = u'Записи в помяннике'


class RequestReminderLink(models.Model):
    reminder = models.ForeignKey(Reminder, verbose_name=u'Помянник', related_name='reminder_requests')
    request = models.ForeignKey('requests.Request', verbose_name=u'Молитвенная просьба')
    date = models.DateTimeField(u'Дата', auto_now_add=True)

    active = models.BooleanField(default=True)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        verbose_name = u'Автоматически добавленная запись'
        verbose_name_plural = u'Автоматически добавленные записи'