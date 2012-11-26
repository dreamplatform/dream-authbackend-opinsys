
import logging
from django.db import models
from dreamuserdb.models import AuthProvider, User
import settings

LOG = logging.getLogger(__name__)

class OpinsysAuthProvider(AuthProvider):
    dc = models.CharField(max_length=200)
    school = models.CharField(max_length=200)
    user = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def _get_ldap_client(self):
        import ldap
        if hasattr(self, 'opinsys_client') and self.opinsys_client != None:
            return self.opinsys_client
        setattr(self, 'opinsys_client', None)
        if settings.CERT_FILE:
            ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, settings.CERT_FILE)
        self.opinsys_client = ldap.initialize(settings.SERVER)
        if settings.USE_TLS:
            self.opinsys_client.start_tls_s()
        dn = 'uid=%s,ou=System Accounts,dc=edu,dc=%s,dc=fi' % (self.user, self.dc)
        try:
            self.opinsys_client.simple_bind_s(dn, self.password)
            return self.opinsys_client
        except ldap.INVALID_CREDENTIALS:
            LOG.exception('Invalid system credentials %s for Opinsys LDAP for organisation %s' % (self.user, self.dc))
            return None

    def get_organisations_for_user(self, remote_uid):
        import ldap
        opinsys_client = self._get_ldap_client()
        search = u'(&(memberUid=%s)(cn=%s)(objectClass=puavoSchool))' % (remote_uid, self.school)
        return opinsys_client.search_s('ou=Groups,dc=edu,dc=%s,dc=fi' % self.dc, ldap.SCOPE_SUBTREE, search)

    def get_user(self, remote_uid):
        import ldap
        opinsys_client = self._get_ldap_client()
        return opinsys_client.search_s('ou=People,dc=edu,dc=%s,dc=fi' %
                self.dc, ldap.SCOPE_SUBTREE, u'(uid=%s)' % remote_uid)

    def authenticate(self, username=None, password=None):
        import ldap
        if not username or not password:
            return False
        opinsys_client = self._get_ldap_client()
        udndata = self.get_user(username)
        if not udndata:
            return False
        try:
            opinsys_client.simple_bind_s(udndata[0][0], password)
            return True
        except ldap.INVALID_CREDENTIALS:
            LOG.error(u'Invalid user credentials %s for Opinsys LDAP for organisation %s' % (username, self.dc))
            return False

    def get_groups_for_user(self, remote_uid):
        import ldap
        opinsys_client = self._get_ldap_client()
        udndata = self.get_user(remote_uid)
        return opinsys_client.search_s('ou=Groups,dc=edu,dc=%s,dc=fi' %
                self.dc, ldap.SCOPE_SUBTREE, '(member=%s)' % udndata[0][0])

    def __unicode__(self):
        return u'%s' % self.school


class OpinsysAssociation(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    remote_uid = models.CharField(max_length=200)
    opinsys_auth_provider = models.ForeignKey(OpinsysAuthProvider)

    class Meta:
        unique_together = ('user', 'remote_uid', 'opinsys_auth_provider')

