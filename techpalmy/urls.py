"""techpalmy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from user import views as user_views

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('django/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('', include('user.urls')),
    path('', include('company.urls')),
    path('events/', include('event.urls')),
	path('admin/', views.Dashboard.as_view(), name='dashboard')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
