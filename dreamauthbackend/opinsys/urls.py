

from django.conf.urls.defaults import *

urlpatterns = patterns('dreamauthbackend.opinsys.views',
        url(r'login/$', 'puavo_login', name='dreamauthbackend_opinsys_login'),
        url(r'register/$', 'puavo_register', name='dreamauthbackend_opinsys_register'),
        url(r'associate/$', 'puavo_associate', name='dreamauthbackend_opinsys_associate'),

)
