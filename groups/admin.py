from django.contrib import admin

# Register your models here.
"""
It should be noted that we are not going to be
using the admin control panel since it is a CMS.
This can be used for testing however!
"""

from django.contrib import admin

from .models import Company, CompanyApplication, Member


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass

@admin.register(CompanyApplication)
class CompanyApplicationAdmin(admin.ModelAdmin):
    pass

@admin.register(Member)
class CompanyMembersAdmin(admin.ModelAdmin):
    pass
