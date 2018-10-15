from django.urls import path

from . import views

app_name = 'event'

urlpatterns = [
    path('', views.events, name='events_listing'),
    path('create', views.CreateEvent.as_view(), name='create_event'),
]
