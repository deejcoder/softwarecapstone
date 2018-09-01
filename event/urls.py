from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'techsite'

urlpatterns = [
    path('events/', views.events, name='events_listing'),
]
