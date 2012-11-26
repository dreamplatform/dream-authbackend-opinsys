
import ldap
from unittest import TestCase
import settings

class OpinsysTestCase(TestCase):
  def _test_connection(self):
    from dreamauthbackend.opinsys.connection import get_ldap_data

    class Org:
      dc = 'kauniainen'
      user = 'haltu'
      password = ''

    r = get_ldap_data(Org(), 'kasavuori.oppilas', 'oppil4s')

    user = r[0]
    print repr(user)

class LDAPTestCase(TestCase):
  def setUp(self):
    server = 'ldaps://extldap1.opinsys.fi:636'

    self.l = ldap.initialize(server)

    dn = "uid=haltu,ou=System Accounts,dc=edu,dc=kauniainen,dc=fi"
    pw = ""

    self.l.simple_bind_s( dn, pw )

  def _test_get_user(self):
    result = self.l.search_s(
      'ou=People,dc=edu,dc=kauniainen,dc=fi',
      ldap.SCOPE_SUBTREE,
      '(uid=kasavuori.oppilas)',
      )

    print repr(result)

  def _test_get_schools(self):
    result = self.l.search_s(
      'ou=Groups,dc=edu,dc=kauniainen,dc=fi',
      ldap.SCOPE_SUBTREE,
      '(&(memberUid=kasavuori.oppilas)(cn=kasavuori)(objectClass=puavoSchool))',
      )

    for r in result:
      print repr(r[1])


  def _test_auth(self):
    import ldap
    server = 'ldaps://extldap1.opinsys.fi:636'

    l = ldap.initialize(server)

    dn = "uid=haltu,ou=System Accounts,dc=edu,dc=kauniainen,dc=fi"
    pw = ""
    upw = 'oppil4s'

    l.simple_bind_s( dn, pw )

    result = l.search_s(
      'ou=People,dc=edu,dc=kauniainen,dc=fi',
      ldap.SCOPE_SUBTREE,
      '(uid=kasavuori.oppilas)',
      )
    
    udn = result[0][0]
    print repr(udn)

    print "2"
    l.simple_bind_s( udn, upw )
    print "3"
    result = l.search_s(
      'ou=People,dc=edu,dc=kauniainen,dc=fi',
      ldap.SCOPE_SUBTREE,
      '(objectClass=*)',
      )
    
    print repr(result)

    result = l.search_s(
      'ou=Groups,dc=edu,dc=kauniainen,dc=fi',
      ldap.SCOPE_SUBTREE,
      '(memberUid=kasavuori.oppilas)',
      )

    for r in result:
      print r[1]['cn']

