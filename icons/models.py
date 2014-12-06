#!-*-coding:utf-8-*-
from django.db import models
from proshumolitv.managers import ActiveManager


class Icon(models.Model):
    name = models.CharField(u'Имя', max_length=255)
    img = models.ImageField(u'Изображение', upload_to='icons')
    description = models.TextField(u'Описание', blank=True)

    active = models.BooleanField(default=True)
    objects = ActiveManager()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Икона'
        verbose_name_plural = u'Иконы'