
import logging
from dreamuserdb.models import User

LOG = logging.getLogger(__name__)

class OpinsysBackend(object):
    supports_anonymous_user = False
    supports_object_permissions = False
    supports_inactive_users = False

    def authenticate(self, username=None, password=None, authprovider=None):
        if not username or not password or not authprovider:
            return None

        is_authenticated = authprovider.authenticate(username=username, password=password)
        if not is_authenticated:
            return None

        udata = authprovider.get_user(username)
        if not udata:
            LOG.exception('Could not get user data from %s to user %s, even when user authentication worked!' %
                    (username, authprovider))
            return None

        udata = udata[0][1]
        user = User(username=udata['uid'][0])
        user.first_name = udata['givenName'][0]
        user.last_name = udata['sn'][0]
        user.set_password('!')
        return user


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
