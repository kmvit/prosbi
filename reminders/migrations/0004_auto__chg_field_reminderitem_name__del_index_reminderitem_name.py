# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Renaming column for 'ReminderItem.name' to match new field type.
        db.delete_column(u'reminders_reminderitem', 'name_id')
        # Changing field 'ReminderItem.name'
        db.add_column(u'reminders_reminderitem', 'name', self.gf('django.db.models.fields.CharField')(max_length=150))
        # Removing index on 'ReminderItem', fields ['name']
        # db.delete_index(u'reminders_reminderitem', ['name_id'])


    def backwards(self, orm):
        # Adding index on 'ReminderItem', fields ['name']
        # db.create_index(u'reminders_reminderitem', ['name_id'])


        # Renaming column for 'ReminderItem.name' to match new field type.
        db.delete_column(u'reminders_reminderitem', 'name')
        # Changing field 'ReminderItem.name'
        db.add_column(u'reminders_reminderitem', 'name_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['names.Name']))

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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
        u'names.name': {
            'Meta': {'ordering': "['nominative']", 'object_name': 'Name'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'genitive': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moderation': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'nominative': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'reminders.reminder': {
            'Meta': {'ordering': "['-permanent', 'title']", 'object_name': 'Reminder'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'account_reminders'", 'to': u"orm['account.Account']"}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permanent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'requests': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'request_reminders'", 'symmetrical': 'False', 'through': u"orm['reminders.RequestReminderLink']", 'to': u"orm['requests.Request']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '3'})
        },
        u'reminders.reminderitem': {
            'Meta': {'object_name': 'ReminderItem'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['requests.Category']", 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_request': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'reminder': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reminder_items'", 'to': u"orm['reminders.Reminder']"})
        },
        u'reminders.requestreminderlink': {
            'Meta': {'object_name': 'RequestReminderLink'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reminder': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reminder_requests'", 'to': u"orm['reminders.Reminder']"}),
            'request': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['requests.Request']"})
        },
        u'requests.category': {
            'Meta': {'object_name': 'Category'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'requests.request': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Request'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'account_requests'", 'to': u"orm['account.Account']"}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'category_requests'", 'to': u"orm['requests.Category']"}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'names': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'name_requests'", 'null': 'True', 'to': u"orm['names.Name']"}),
            'old_names': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'old_prayer_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['reminders']