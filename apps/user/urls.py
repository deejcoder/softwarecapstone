"""
Simply defines the URL mapping for user profiles, user/<username>/
"""
from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('user/<username>/', views.Profile.as_view(), name='user_profile'),
    path('user/<username>/edit/', views.EditProfile.as_view(), name='user_profile_edit'),
    path('consultants/', views.Listing.as_view(), name='consultants'),
    path('consultants/apply/', views.Apply.as_view()),
    path('register/', views.Register.as_view(), name="register"),
]
