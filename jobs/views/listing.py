"""
Lists all jobs, allows companies to add new jobs
"""

from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from jobs.models import Job
from jobs.forms import JobCreationForm


class Listing(View):

    def get(self, request):

        # search ---
        search_term = request.GET.get('search')
        if search_term is not None:
            jobs = Job.search_jobs(search_term)

        else:
            jobs = Job.search_jobs(None)
        # ---

        # filters ---
        location = request.GET.get('location')
        company = request.GET.get('company')

        if location is not None:
            jobs = jobs.filter(location=location)
        
        if company is not None:
            jobs = jobs.filter(company=company)
        # ---

        # pages (6 jobs/page) ---
        paginator = Paginator(jobs, 6)
        page = request.GET.get('page')
        show_jobs = paginator.get_page(page)
        # ---

        create_job_form = JobCreationForm()

        return render(request, 'jobs.html', {
            'jobs': show_jobs,
            'page': page,
            'creation_form': create_job_form
        })
