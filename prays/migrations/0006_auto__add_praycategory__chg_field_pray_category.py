# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PrayCategory'
        db.create_table(u'prays_praycategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('index', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
        ))
        db.send_create_signal(u'prays', ['PrayCategory'])

        # Adding M2M table for field tags on 'Pray'
        m2m_table_name = db.shorten_name(u'prays_pray_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pray', models.ForeignKey(orm[u'prays.pray'], null=False)),
            ('category', models.ForeignKey(orm[u'requests.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pray_id', 'category_id'])


        # Changing field 'Pray.category'
        db.alter_column(u'prays_pray', 'category_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prays.PrayCategory']))

    def backwards(self, orm):
        # Deleting model 'PrayCategory'
        db.delete_table(u'prays_praycategory')

        # Removing M2M table for field tags on 'Pray'
        db.delete_table(db.shorten_name(u'prays_pray_tags'))


        # Changing field 'Pray.category'
        db.alter_column(u'prays_pray', 'category_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['requests.Category']))

    models = {
        u'account.account': {
            'Meta': {'object_name': 'Account'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'anonym': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'confession': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'confession_accounts'", 'null': 'True', 'to': u"orm['account.Confession']"}),
            'days_for_reminder': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '7'}),
            'dignity': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'dignity_accounts'", 'null': 'True', 'to': u"orm['account.Dignity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'name_accounts'", 'null': 'True', 'to': u"orm['names.Name']"}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'account.confession': {
            'Meta': {'object_name': 'Confession'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'account.dignity': {
            'Meta': {'object_name': 'Dignity'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'short': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'icons.icon': {
            'Meta': {'object_name': 'Icon'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'names.name': {
            'Meta': {'ordering': "['nominative']", 'object_name': 'Name'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'genitive': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'genitive_church': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moderation': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'nominative': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'})
        },
        u'prays.pray': {
            'Meta': {'object_name': 'Pray'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'praycategory_prays'", 'to': u"orm['prays.PrayCategory']"}),
            'icons': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['icons.Icon']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'markdown_text': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'category_prays'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['requests.Category']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'prays.praycategory': {
            'Meta': {'ordering': "['index']", 'object_name': 'PrayCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'prays.prayerbook': {
            'Meta': {'object_name': 'PrayerBook'},
            'account': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'prayerbook'", 'unique': 'True', 'to': u"orm['account.Account']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prays': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['prays.Pray']", 'through': u"orm['prays.PrayerBookItem']", 'symmetrical': 'False'})
        },
        u'prays.prayerbookitem': {
            'Meta': {'ordering': "['index']", 'object_name': 'PrayerBookItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'pray': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['prays.Pray']"}),
            'prayerbook': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prayerbook_items'", 'to': u"orm['prays.PrayerBook']"})
        },
        u'requests.category': {
            'Meta': {'object_name': 'Category'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        }
    }

    complete_apps = ['prays']