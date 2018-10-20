from django.urls import path
from django.conf.urls import url
from .views import company
from .views import group
from .views import get_members
from .views.group.profile import group_remove
from .views.company.profile import company_remove

app_name = "entity"

urlpatterns = [
    path('company/apply', company.ApplyCompany.as_view(), name='company_application'),
    path('company/<company>/edit', company.EditProfile.as_view(), name='company_application'),
    path('companies/', company.Listing.as_view(), name='company_listing'),
    path('company/<company>/', company.Profile.as_view(), name='company_profile'),
    path('company/<company>/remove/', company_remove, name='remove_group'),
    path('groups/', group.Listing.as_view(), name='group_listing'),
    path('groups/apply/', group.Apply.as_view(), name='group_apply'),
    path('groups/<group>/', group.profile.Profile.as_view(), name='group_profile'),
    path('groups/<group>/edit', group.profile.EditProfile.as_view(), name='group_profile_edit'),
    path('groups/<group>/remove/', group_remove, name='remove_group'),
    # only restrict the below URL 'entity' to groups or companies
    url(r'^(?P<entity>groups|companies)/(?P<entity_name>[\w|\W]{0,20})/members', get_members, name='group_members'),
]
