# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'OpinsysAuthProvider.school'
        db.add_column('opinsys_opinsysauthprovider', 'school', self.gf('django.db.models.fields.CharField')(default='', max_length=200), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'OpinsysAuthProvider.school'
        db.delete_column('opinsys_opinsysauthprovider', 'school')


    models = {
        'dreamuserdb.authprovider': {
            'Meta': {'object_name': 'AuthProvider'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organisation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'auth_providers'", 'to': "orm['dreamuserdb.Organisation']"})
        },
        'dreamuserdb.organisation': {
            'Meta': {'object_name': 'Organisation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'opinsys.opinsysauthprovider': {
            'Meta': {'object_name': 'OpinsysAuthProvider', '_ormbases': ['dreamuserdb.AuthProvider']},
            'authprovider_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['dreamuserdb.AuthProvider']", 'unique': 'True', 'primary_key': 'True'}),
            'dc': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['opinsys']
