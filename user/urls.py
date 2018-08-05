from django.urls import include, path
from . import views

app_name = 'user'
urlpatterns = [
    path('<username>/', views.Profile.as_view())
]