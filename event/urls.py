from django.urls import path

from . import views

app_name = 'event'

urlpatterns = [
    path('', views.events, name='events_listing'),
]
