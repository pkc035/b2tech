from django.contrib import admin
from .models        import SharedGroup, GroupInvitation

admin.site.register(SharedGroup)
admin.site.register(GroupInvitation)
