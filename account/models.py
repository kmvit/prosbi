#!-*-coding:utf-8-*-
from random import choice
from django.contrib.auth.models import User
from django.db import models
from account.settings import DAYS_FOR_REMINDER
from names.models import Name
from proshumolitv.managers import ActiveManager
from reminders.models import Reminder


class Account(models.Model):
    user = models.OneToOneField(User, related_name='account', null=True, blank=True)
    token = models.CharField(max_length=255)
    name = models.ForeignKey(Name, verbose_name=u'Имя', related_name='name_accounts', null=True, blank=True)
    dignity = models.ForeignKey('Dignity', verbose_name=u'Сан', related_name='dignity_accounts', null=True, blank=True)
    confession = models.ForeignKey('Confession', verbose_name=u'Конфессия', related_name='confession_accounts', null=True, blank=True)

    anonym = models.BooleanField(u'Незарегистрированный', default=False)

    days_for_reminder = models.PositiveSmallIntegerField(u'Дней для хранения записи в помяннике', choices=DAYS_FOR_REMINDER, default=7)

    active = models.BooleanField(u'Активно', default=True)
    objects = ActiveManager()

    class Meta:
        verbose_name = u'Аккаунт'
        verbose_name_plural = u'Аккаунты'

    def __unicode__(self):
        return self.user.username if self.user else self.token

    def get_name(self):
        return self.name.nominative if self.name else u'Аноним'

    def get_dignity(self):
        return self.dignity.name if self.dignity else None

    @property
    def moderation(self):
        return self.name.moderation

    @classmethod
    def create_raw_account(cls, request):
        """
        Creates raw user object and get or create account object on sign up
        """
        email = request.POST.get('email', None)
        if not email or User.objects.filter(username__iexact=email).exists():
            return None
        password = "".join([choice("abcdefghijklmnopqrstuvwxyz1234567890") for i in xrange(10)])
        token = request.session.session_key
        if not token:
            request.session.modified = True
        user = User(username=email.lower(), email=email.lower(), is_active=False)
        user.set_password(password)
        user.save()
        account, created = Account.objects.get_or_create(token=token)
        account.user = user
        account.save()
        Reminder.create_defaults(account)
        from prays.models import PrayerBook
        PrayerBook.create_defaults(account)
        return account

    @classmethod
    def create_random_account(cls):
        account = Account.objects.create(anonym=True, token="".join([choice("abcdefghijklmnopqrstuvwxyz1234567890") for _ in xrange(10)]))
        return account

    @classmethod
    def get_account(cls, request):
        if not request.session.exists(request.session.session_key):
            request.session.create()
        if request.user.is_authenticated():
            try:
                return Account.objects.get(user=request.user)
            except Account.DoesNotExist:
                account, created = Account.objects.get_or_create(token=request.session.session_key)
                account.user = request.user
                account.anonym = False
                account.save()
                Reminder.create_defaults(account)
                from prays.models import PrayerBook
                PrayerBook.create_defaults(account)
                return account
            except Exception:
                return None
        else:
            account, created = Account.objects.get_or_create(anonym=True, token=request.session.session_key)
            Reminder.create_defaults(account)
            return account


class Dignity(models.Model):
    name = models.CharField(u'Наименование', max_length=100)
    short = models.CharField(u'Сокращенное наименование', max_length=100, blank=True)

    active = models.BooleanField(u'Активно', default=True)
    objects = ActiveManager()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Сан'
        verbose_name_plural = u'Саны'


class Confession(models.Model):
    name = models.CharField(u'Наименование', max_length=100)

    active = models.BooleanField(u'Активно', default=True)
    objects = ActiveManager()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Конфессия'
        verbose_name_plural = u'Конфессии'


class Social(models.Model):
    account = models.ForeignKey(Account, verbose_name=u'Аккаунт', related_name='account_socials')
    url = models.CharField(u'Ссылка на профиль', max_length=255)
    social_network = models.ForeignKey('SocialNetwork', verbose_name=u'Социальная сеть')

    def __unicode__(self):
        return self.url

    class Meta:
        verbose_name = u'Ссылка на соцсеть'
        verbose_name_plural = u'Ссылки на соцсети'


class SocialNetwork(models.Model):
    name = models.CharField(u'Наименование', max_length=100)
    url = models.CharField(u'Адрес', max_length=150, null=True, blank=True)

    active = models.BooleanField(u'Активно', default=True)
    objects = ActiveManager()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Соцсеть'
        verbose_name_plural = u'Соцсети'
