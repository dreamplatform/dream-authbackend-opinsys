
from django.contrib import admin
from dreamauthbackend.opinsys.models import OpinsysAuthProvider, OpinsysAssociation

class OpinsysAuthProviderAdmin(admin.ModelAdmin):
  list_display = ('organisation', 'dc', 'school', 'user')
  list_filter = ('organisation',)

admin.site.register(OpinsysAuthProvider, OpinsysAuthProviderAdmin)
admin.site.register(OpinsysAssociation)

