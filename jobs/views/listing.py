"""
Lists all jobs, allows companies to add new jobs
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from entity.models import Member
from jobs.forms import JobCreationForm
from jobs.models import Job


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
            'show_sidepane': Member.is_editor_any(request.user) ^ Member.is_owner_any(request.user),
            'jobs': show_jobs,
            'page': page,
            'creation_form': create_job_form
        })

    @method_decorator(login_required)
    def post(self, request):
        form = JobCreationForm(request.POST)
        if form.is_valid():
            job = form.save(commit=True)
            messages.success(request, "Your new job has been created!")
            return HttpResponseRedirect(reverse('jobs:job_details', args=[job.title, job.id]))
        return HttpResponseRedirect(reverse('jobs:job_listing'))
