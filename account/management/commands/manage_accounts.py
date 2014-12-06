# -*- coding: utf-8 -*-
from random import choice

from django.db.models import Count, Avg
from account.models import Account
from django.core.management.base import NoArgsCommand, BaseCommand


class Command(NoArgsCommand):
    help = 'Week winners'

    def handle(self, *args, **options):
        tokens = Account.all_objects.values('token').annotate(token_count=Count('token')).filter(token_count__gte=2).order_by('-token_count')
        accounts = Account.all_objects.filter(token__in=[t['token'] for t in tokens], anonym=True)
        for a in accounts:
            a.token = "".join([choice("abcdefghijklmnopqrstuvwxyz1234567890") for i in xrange(10)])
            a.save()
        self.stdout.write('Accounts processed')
