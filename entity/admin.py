from django.contrib import admin

from entity.models import Member, Application, company


@admin.register(company.Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(Application)
class CompanyApplicationAdmin(admin.ModelAdmin):
    pass


@admin.register(Member)
class CompanyMembersAdmin(admin.ModelAdmin):
    pass
