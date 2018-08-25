"""
It should be noted that we are not going to be
using the admin control panel since it is a CMS.
This can be used for testing however!
"""

from django.contrib import admin

from .models import Consultant, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Consultant)
class ConsultantAdmin(admin.ModelAdmin):
    pass
