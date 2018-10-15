"""
Lists all jobs, allows companies to add new jobs
"""
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views import View

from jobs.models import Job


class Detail(View):

    def get(self, request, job_title, job_id):

        try: 
            job = Job.objects.get(pk=job_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

        return render(request, 'jobs/details.html', {
            'job': job,
        })
