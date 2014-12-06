# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Name'
        db.create_table(u'names_name', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nominative', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('genitive', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('moderation', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'names', ['Name'])


    def backwards(self, orm):
        # Deleting model 'Name'
        db.delete_table(u'names_name')


    models = {
        u'names.name': {
            'Meta': {'object_name': 'Name'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'genitive': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moderation': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'nominative': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['names']