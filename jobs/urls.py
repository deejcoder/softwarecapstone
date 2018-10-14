from django.urls import path
from django.conf.urls import url

from jobs.views import Listing

app_name = "jobs"

urlpatterns = [
    path('jobs/', Listing.as_view(), name='job_listing'),
]
