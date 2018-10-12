from django.contrib import admin

from entity.models import Member, Application, company, group


@admin.register(company.Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(Application)
class CompanyApplicationAdmin(admin.ModelAdmin):
    pass


@admin.register(Member)
class CompanyMembersAdmin(admin.ModelAdmin):
    pass


@admin.register(group.Group)
class GroupAdmin(admin.ModelAdmin):
    pass
