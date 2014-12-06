# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Name.genitive_church'
        db.add_column(u'names_name', 'genitive_church',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=150, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Name.genitive_church'
        db.delete_column(u'names_name', 'genitive_church')


    models = {
        u'names.name': {
            'Meta': {'ordering': "['nominative']", 'object_name': 'Name'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'genitive': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'genitive_church': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moderation': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'nominative': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['names']