from django.urls import path

from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.Index.as_view()),
    path('users', views.Users.as_view()),
    path('consultants', views.Consultants.as_view()),
    path('companies', views.Companies.as_view()),
    path('companies/applications', views.CompanyApplications.as_view()),
]
