#!-*-coding:utf-8-*-
from django.db import models
from markdown import markdown
from icons.models import Icon
from proshumolitv.managers import ActiveManager
from requests.models import Category


class Pray(models.Model):
    tags = models.ManyToManyField(Category, verbose_name=u'Тэги', related_name='category_prays', null=True, blank=True)
    category = models.ForeignKey('PrayCategory', verbose_name=u'Категория', related_name='praycategory_prays')
    name = models.CharField(u'Наименование', max_length=150)
    slug = models.CharField(u'Ссылка', max_length=255, blank=True)
    markdown_text = models.TextField(u'Текст')
    text = models.TextField(u'Отображаемый текст', editable=False)
    icons = models.ManyToManyField(Icon, verbose_name=u'Иконы', null=True, blank=True)

    active = models.BooleanField(u'Активно', default=True)
    objects = ActiveManager()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        overriding for markdown field
        """
        self.text = markdown(self.markdown_text)
        self.translit_slug()
        super(Pray, self).save(*args, **kwargs)

    def translit_slug(self):
        symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
           u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")
        # tr = {ord(a):ord(b) for a, b in zip(*symbols)}
        tr = dict([(ord(a), ord(b)) for (a, b) in zip(*symbols)])
        self.slug = self.name.translate(tr).replace(' ', '_')

    class Meta:
        verbose_name = u'Молитва'
        verbose_name_plural = u'Молитвы'


class PrayCategory(models.Model):
    name = models.CharField(u'Название', max_length=150)
    index = models.PositiveSmallIntegerField(u'Порядковый номер', default=1)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['index']
        verbose_name = u'Категория молитв'
        verbose_name_plural = u'Категории молитв'


class PrayerBook(models.Model):
    account = models.OneToOneField('account.Account', verbose_name=u'Молитвослов', related_name='prayerbook')
    prays = models.ManyToManyField(Pray, through='PrayerBookItem')

    def __unicode__(self):
        return u'Молитвослов #{}'.format(self.id)

    @classmethod
    def create_defaults(cls, account):
        pb, created = cls.objects.get_or_create(account=account)
        return pb

    def add_pray(self, pray):
        if pray not in self.prays.all():
            index = self.prays.count() + 1
            item = PrayerBookItem.objects.create(prayerbook=self, pray=pray, index=index)
            return item

    def pray_added(self, pray):
        return pray in self.prays.all()

    class Meta:
        verbose_name = u'Молитвослов'
        verbose_name_plural = u'Молитвословы'


class PrayerBookItem(models.Model):
    prayerbook = models.ForeignKey(PrayerBook, verbose_name=u'Молитвослов', related_name='prayerbook_items')
    pray = models.ForeignKey(Pray, verbose_name=u'Молитва')
    index = models.PositiveSmallIntegerField(u'Порядковый номер', default=1)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        ordering = ['index']