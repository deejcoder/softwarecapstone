from django.urls import path

from . import views

app_name = 'event'

urlpatterns = [
    path('', views.events, name='events_listing'),
    path('create', views.CreateEvent.as_view(), name='create_event'),
    path('<event_title>-<event_id>/', views.EventDetails.as_view(), name='event_details'),
    path('<event_title>-<event_id>/remove', views.remove_event, name="remove_event")
]
