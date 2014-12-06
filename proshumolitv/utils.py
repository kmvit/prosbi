#!-*coding:utf-8*-
import csv
from time import strptime, mktime
from datetime import datetime
from account.models import Account
from reminders.settings import REMINDER_TYPES, FOR_REPOSE_TYPE, FOR_HEALTH_TYPE
from requests.models import PrayEvent, Category, Request


def import_requests():
    with open('sb_plugins_5.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

        account = Account.create_random_account()

        for row in spamreader:
            cat_, names, text, date, count = row
            cat_ = cat_.decode('utf-8')

            try:
                d = strptime(date, "%a, %d %b %Y %H:%M:%S +0300")
            except:
                d = strptime(date[:-6], "%a, %d %b %Y %H:%M:%S")

            dt = datetime.fromtimestamp(mktime(d))

            try:
                count = int(count)
            except:
                count = 0

            if cat_ == u'О упокоении':
                cat_ = u'Об упокоении'

            type = FOR_REPOSE_TYPE if cat_ == u'Об упокоении' else FOR_HEALTH_TYPE
            try:
                cat = Category.objects.get(name=cat_)
            except:
                cat = Category.objects.create(name=cat_, type=type)

            try:
                p = Request.objects.create(
                    category=cat,
                    account=account,
                    comment=text if text != 'NULL' else '',
                    old_names=names[:255],
                    old_prayer_count=count
                )

                p.date = dt
                p.save()

            except:
                continue

            print p