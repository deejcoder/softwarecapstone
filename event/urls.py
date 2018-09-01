from django.urls import path

from . import views

app_name = 'techsite'

urlpatterns = [
    path('events/', views.events, name='events_listing'),
]
