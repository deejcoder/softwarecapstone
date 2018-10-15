from django.urls import path
from django.conf.urls import url

from jobs.views import Listing
from jobs.views import Detail

app_name = "jobs"

urlpatterns = [
    path('jobs/', Listing.as_view(), name='job_listing'),
    path('jobs/<job_title>-<job_id>/', Detail.as_view(), name='job_details'),
]
