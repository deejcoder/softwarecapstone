from django.urls import path
from .views import company

app_name = "company"

urlpatterns = [
    path('company/apply', company.ApplyCompany.as_view(), name='company_application'),
    path('company/profile/edit', company.edit_comp, name='company_application'),
    path('companies/', company.Listing.as_view(), name='company_listing'),
    path('company/<company>/', company.Profile.as_view(), name='company_profile'),
]
