from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'techsite'

urlpatterns = [
    path('', views.index, name='index'),
    path('company/apply', views.company, name='company_application'),
    path('events/', views.events, name='events_listing'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.login, {'template_name': 'login.html'}, name='login'),
    path('consultants/', views.listing, name='consultants'),
    path('consultants/apply', views.Apply.as_view()),
    path('user/<username>/', views.Profile.as_view(), name="user_profile"),
]
