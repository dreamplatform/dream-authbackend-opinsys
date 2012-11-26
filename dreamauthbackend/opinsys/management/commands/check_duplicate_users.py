# -*- coding: utf-8 -*-

from optparse import make_option
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User as DjangoUser
from dreamauthbackend.opinsys.models import OpinsysAuthProvider
from dreamauthbackend.opinsys import settings
import ldap

class Command(BaseCommand):
  def handle(self, *args, **options):
    for config in OpinsysAuthProvider.objects.all():
      dc = config.dc
      user = config.user
      pw = config.password
      server = settings.SERVER
      dn = 'uid=%s,ou=System Accounts,dc=edu,dc=%s,dc=fi' % (user, dc) 

      c = ldap.initialize(server)
      if settings.USE_TLS:
        c.start_tls_s()

      try:
        c.simple_bind_s(dn, pw) 
      except ldap.INVALID_CREDENTIALS:
        print "ERR"
    
      for user in DjangoUser.objects.all():

        udndata = c.search_s('ou=People,dc=edu,dc=%s,dc=fi' % dc, ldap.SCOPE_SUBTREE, '(uid=%s)' % user.username)
  
        if len(udndata) > 0:
          print '%s:%s: %s' % (config.id, config.organisation.name, user.username)


