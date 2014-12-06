#!-*-coding:utf-8-*-
from django.db import models
from proshumolitv.managers import ActiveManager


class ModeratedManager(models.Manager):
    def get_queryset(self):
        return super(ModeratedManager, self).get_queryset().filter(moderated=True)


class Name(models.Model):
    nominative = models.CharField(u'Имя', max_length=150, blank=True)
    genitive = models.CharField(u'Имя в родительном падеже', max_length=150)
    genitive_church = models.CharField(u'Церковная форма имя в родительном падеже', max_length=150, blank=True)

    moderation = models.BooleanField(u'На модерации', default=True)
    active = models.BooleanField(u'Активно', default=True)

    objects = ActiveManager()
    moderated = ModeratedManager()

    def __unicode__(self):
        return self.nominative

    class Meta:
        ordering = ['nominative']
        verbose_name = u'Имя'
        verbose_name_plural = u'Имена'