

import logging
from django.db import IntegrityError
from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate
from dreamauthbackend.opinsys.models import OpinsysAuthProvider, OpinsysAssociation


LOG = logging.getLogger(__name__)


class PuavoAuthenticationForm(forms.Form):
    username = forms.CharField(label=_(u'Username'), max_length=200)
    password = forms.CharField(label=_(u'Password'), widget=forms.PasswordInput)
    school = forms.ModelChoiceField(label=_('School'), queryset=OpinsysAuthProvider.objects.all())

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        school = self.cleaned_data.get('school')
        if username and password and school:
            self._user = authenticate(username=username, password=password, authprovider=school)
            if not self._user:
                raise forms.ValidationError(
                            _(u'Invalid username/password.'))
            self.user_data = school.get_user(username)
            if not self.user_data:
                raise forms.ValidationError('user %s was authenticated to %s, yet fetchin userdata failed' % 
                        (username, school))
        return self.cleaned_data

    def _update_user(self, user, remote_uid, update_user=True, update_groups=True,
                    update_roles=True, update_organisation=True):
        """
        Call this explicitly when userdata, groups or organisation needs to be synced from ldap
        Use only after allvalidations 

        :param user: local user object
        :param remote_uid: users uid in ldap
        """
        school = self.cleaned_data.get('school')
        if not school or not self._user:
            raise Exception('_update_user() must be called ONLY after data validation')
        if update_user:
            # TODO update user fields, maybe? this needs some further thinking as this would override
            # user submitted values, from profile dialog example
            pass
        if update_groups:
            group_data = school.get_groups_for_user(remote_uid)
            if group_data:
                for group in group_data[0]:
                    gn = group[1]['cn'][0]
                    LOG.debug('Trying to add user %s to group %s' % (user, gn))
                    groups_in_org = school.organisation.groups.filter(name=gn, official=True)
                    for g in groups_in_org:
                        user.user_groups.add(g)
                        LOG.debug('Added user %s to group %s' % (user, g))
        if update_roles:
            for rn in self.user_data[0][1]['puavoEduPersonAffiliation']:
                LOG.debug('Trying to add user %s to role %s' % (user, rn))
                roles_in_org = school.organisation.role_set.filter(name=rn, official=True)
                for role in roles_in_org:
                    user.roles.add(role)
                    LOG.debug('Added user %s to role %s' % (user, role))
        if update_organisation:
            org = school.organisation
            user.organisations.add(org)
            LOG.debug('Added user %s to organisation %s' % (user, org))


class PuavoLoginForm(PuavoAuthenticationForm):
    def clean(self):
        super(PuavoLoginForm, self).clean()
        username = self.cleaned_data.get('username') # remote_id
        school = self.cleaned_data.get('school')
        if username and school:
            try:
                self.association = OpinsysAssociation.objects.get(remote_uid=username,
                        opinsys_auth_provider=school)
                self.association.user.backend = self._user.backend
                self._update_user(self.association.user, username)
            except OpinsysAssociation.DoesNotExist:
                raise forms.ValidationError(
                        _(u'''Before you can login with Puavo, you need to associate your account
                            with Puavo authentication provider. If you don\'t have account, you can create new one
                            in register page'''))


class PuavoRegisterForm(PuavoAuthenticationForm):
    # TODO format validation and format instructions to help text
    new_username = forms.CharField(label=_(u'username to this service'), required=False,
            help_text=_('''This will be your username to #serivice. It will be used for example when system 
                automatically creates mail account to you'''))

    def __init__(self, *args, **kwargs):
        self.require_new_username = False
        return super(PuavoRegisterForm, self).__init__(*args, **kwargs)

    def clean(self):
        super(PuavoRegisterForm, self).clean()
        username = self.cleaned_data.get('username') # remote_id
        school = self.cleaned_data.get('school')
        if username and school:
            try:
                OpinsysAssociation.objects.get(remote_uid=username, opinsys_auth_provider=school)
                raise forms.ValidationError(
                            _('Your account is already associated with this Puavo authentication provider. Just use login'))
            except OpinsysAssociation.DoesNotExist:
                pass

            udata = self.user_data[0][1]
            user = self._user
            _username = self.cleaned_data.get('new_username', None)
            if not _username:
                _username = udata['uid'][0]
            user.username = _username
            user.first_name = udata['givenName'][0]
            user.last_name = udata['sn'][0]
            user.set_password('!')

            try:
                user.save()
            except IntegrityError:
                self.require_new_username = True
                raise forms.ValidationError(_(u'Username is already in use. Please provide a new one.'))

            self.association = OpinsysAssociation(user=user, opinsys_auth_provider=school, remote_uid=udata['uid'][0])
            self.association.save()
            self._update_user(user, self.association.remote_uid)
            self.user = user
            return self.cleaned_data


class PuavoAssociateForm(PuavoAuthenticationForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        return super(PuavoAssociateForm, self).__init__(*args, **kwargs)

    def clean(self):
        super(PuavoAssociateForm, self).clean()
        if not self.errors:
            username = self.cleaned_data.get('username') # remote_id
            school = self.cleaned_data.get('school')
            try:
                OpinsysAssociation(user=self.user, opinsys_auth_provider=school, remote_uid=username).save()
                self._update_user(self.user, username)
            except IntegrityError:
                raise forms.ValidationError(_('Your account is already associated with this Puavo authentication provider.'))
        return self.cleaned_data
