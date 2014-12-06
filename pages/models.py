#!-*-coding:utf-8-*-
from django.db import models
from markdown import markdown


class Page(models.Model):
    url = models.CharField(u'URL', max_length=100)
    title = models.CharField(u'Заголовок', max_length=255)
    markdown_content = models.TextField(u'Контент', blank=True)
    content = models.TextField(u'Отображаемый контент', blank=True, editable=False)

    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        overriding for markdown field
        """
        self.content = markdown(self.markdown_content)
        super(Page, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u'Страница'
        verbose_name_plural = u'Страницы'