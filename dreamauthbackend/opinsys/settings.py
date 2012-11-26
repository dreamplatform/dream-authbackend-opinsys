
import os
from django.conf import settings

BASEDIR = os.path.dirname(os.path.abspath(__file__))

SERVER = getattr(settings, 'DREAMAUTHBACKEND_OPINSYS_SERVER', 'ldap://extldap1.opinsys.fi:389')
USE_TLS = getattr(settings, 'DREAMAUTHBACKEND_OPINSYS_USE_TLS', True)
CERT_FILE = getattr(settings, 'DREAMAUTHBACKEND_OPINSYS_CERT_FILE', os.path.join(BASEDIR, 'opinsys-ca.crt'))

