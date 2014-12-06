#!-*-coding:utf-8-*-
from django.db import models
from markdown import markdown
from account.models import Account
from names.models import Name
from proshumolitv.managers import ActiveManager
from reminders.settings import REMINDER_TYPES
from django.db.models import Q


class ModeratedManager(models.Manager):
    def get_queryset(self):
        moderation_names = Name.objects.filter(moderation=True)
        return super(ModeratedManager, self).get_queryset().filter(Q(names__isnull=True, old_names__isnull=False) | Q(names__isnull=False)).exclude(names__in=moderation_names).distinct()

class Request(models.Model):
    category = models.ForeignKey('Category', verbose_name=u'Категория', related_name='category_requests')
    account = models.ForeignKey(Account, verbose_name=u'Просящий', related_name='account_requests')
    names = models.ManyToManyField(Name, verbose_name=u'Имена', related_name='name_requests', null=True)
    # markdown_comment = models.TextField(u'Комментарий', blank=True, null=True)
    comment = models.TextField(u'Комментарий', blank=True, null=True)
    date = models.DateTimeField(u'Дата', auto_now_add=True)

    #imported data from old bd
    old_names = models.CharField(u'Имена', max_length=255, blank=True, null=True)
    old_prayer_count = models.PositiveSmallIntegerField(u'Количество молящихся', default=0)

    active = models.BooleanField(u'Активно', default=True)
    objects = ActiveManager()
    moderated = ModeratedManager()

    def __unicode__(self):
        return str(self.id)
        # return u'Просьба №{0}. {1} {2}'.format(self.id, self.category.name, u', '.join([o.genitive for o in self.names.all()]))

    def get_names_string(self):
        if self.old_names:
            return self.old_names
        return u', '.join([i.genitive for i in self.names.all()])

    def get_prayer_count(self):
        return self.request_prayevents.count() + self.old_prayer_count

    def has_names_on_moderation(self):
        return self.names.filter(moderation=True).exists()
        
    def is_prayer(self, account): 
        return self.request_prayevents.filter(prayer=account).exists() 
 
    def get_prayers(self): 
        return Account.objects.filter(pk__in=[a.prayer.id for a in self.request_prayevents.all()]) 


    class Meta:
        ordering = ['-date']
        verbose_name = u'Молитвенная просьба'
        verbose_name_plural = u'Молитвенные просьбы'
 

class Category(models.Model):
    name = models.CharField(u'Наименование', max_length=100)
    type = models.PositiveSmallIntegerField(u'Тип', choices=REMINDER_TYPES)

    active = models.BooleanField(u'Активно', default=True)
    objects = ActiveManager()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Категория'
        verbose_name_plural = u'Категории'


class PrayEvent(models.Model):
    request = models.ForeignKey(Request, verbose_name=u'Молитвенная просьба', related_name='request_prayevents')
    prayer = models.ForeignKey(Account, verbose_name=u'Молящийся', related_name='account_prayevents')
    date = models.DateTimeField(u'Дата', auto_now_add=True)

    active = models.BooleanField(u'Активно', default=True)
    objects = ActiveManager()

    def __unicode__(self):
        return u'{prayer} помолится {category} {name}'.format(
            prayer=self.prayer.get_name(),
            category=self.request.category.name,
            name=u', '.join([o.genitive for o in self.request.names.all()]))

    class Meta:
        verbose_name = u'Событие "Помолюсь"'
        verbose_name_plural = u'События "Помолюсь"'


class Comment(models.Model):
    request = models.ForeignKey(Request, verbose_name=u'Просьба', related_name='request_comments')
    account = models.ForeignKey(Account, verbose_name=u'Автор', related_name='account_comments')
    date = models.DateTimeField(u'Дата', auto_now_add=True)
    text = models.TextField(u'Текст')

    moderation = models.BooleanField(u'На модерации', default=False)
    active = models.BooleanField(u'Активно', default=True)
    objects = ActiveManager()

    def __unicode__(self):
        return self.text

    class Meta:
        verbose_name = u'Комментарий'
        verbose_name_plural = u'Комментарии'
