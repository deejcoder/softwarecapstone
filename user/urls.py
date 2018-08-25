"""
Simply defines the URL mapping for user profiles, user/<username>/
"""
from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('<username>/', views.Profile.as_view())
]
