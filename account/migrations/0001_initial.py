# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Account'
        db.create_table(u'account_account', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True, blank=True)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='name_accounts', null=True, to=orm['account.Name'])),
            ('dignity', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='dignity_accounts', null=True, to=orm['account.Dignity'])),
            ('confession', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='confession_accounts', null=True, to=orm['account.Confession'])),
            ('anonym', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'account', ['Account'])

        # Adding model 'Name'
        db.create_table(u'account_name', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nominative', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('genitive', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('moderation', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'account', ['Name'])

        # Adding model 'Dignity'
        db.create_table(u'account_dignity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'account', ['Dignity'])

        # Adding model 'Confession'
        db.create_table(u'account_confession', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'account', ['Confession'])

        # Adding model 'Social'
        db.create_table(u'account_social', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='account_socials', to=orm['account.Account'])),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('social_network', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.SocialNetwork'])),
        ))
        db.send_create_signal(u'account', ['Social'])

        # Adding model 'SocialNetwork'
        db.create_table(u'account_socialnetwork', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'account', ['SocialNetwork'])


    def backwards(self, orm):
        # Deleting model 'Account'
        db.delete_table(u'account_account')

        # Deleting model 'Name'
        db.delete_table(u'account_name')

        # Deleting model 'Dignity'
        db.delete_table(u'account_dignity')

        # Deleting model 'Confession'
        db.delete_table(u'account_confession')

        # Deleting model 'Social'
        db.delete_table(u'account_social')

        # Deleting model 'SocialNetwork'
        db.delete_table(u'account_socialnetwork')


    models = {
        u'account.account': {
            'Meta': {'object_name': 'Account'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'anonym': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'confession': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'confession_accounts'", 'null': 'True', 'to': u"orm['account.Confession']"}),
            'dignity': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'dignity_accounts'", 'null': 'True', 'to': u"orm['account.Dignity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'name_accounts'", 'null': 'True', 'to': u"orm['account.Name']"}),
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
        u'account.name': {
            'Meta': {'object_name': 'Name'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'genitive': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moderation': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'nominative': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'account.social': {
            'Meta': {'object_name': 'Social'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'account_socials'", 'to': u"orm['account.Account']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'social_network': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.SocialNetwork']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'account.socialnetwork': {
            'Meta': {'object_name': 'SocialNetwork'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'})
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
        }
    }

    complete_apps = ['account']