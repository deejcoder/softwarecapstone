from django.urls import path
from . import views

app_name = "company"

urlpatterns = [
    path('company/apply', views.ApplyCompany.as_view(), name='company_application'),
    path('company/profile/edit', views.edit_comp, name='company_application'),
]
