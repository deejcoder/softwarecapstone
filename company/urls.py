from django.urls import path
from . import views

app_name = "company"

urlpatterns = [
    path('company/apply', views.company, name='company_application'),
]
