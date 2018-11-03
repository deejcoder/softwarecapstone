from django.urls import path
from django.conf.urls import url

from .views import Listing
from .views import Detail
from .views import EditDetails
from .views import remove_job

app_name = "jobs"

urlpatterns = [
    path('jobs/', Listing.as_view(), name='job_listing'),
    path('jobs/<job_title>-<job_id>/', Detail.as_view(), name='job_details'),
    path('jobs/<job_title>-<job_id>/edit/', EditDetails.as_view(), name='edit_job'),
    path('jobs/<job_title>-<job_id>/remove/', remove_job, name='remove_job'),
]
