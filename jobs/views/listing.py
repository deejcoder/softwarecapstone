"""
Lists all jobs, allows companies to add new jobs
"""

from django.core.paginator import Paginator
from django.shortcuts import render
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

        # determine if the user is an editor of any company
        try:
            is_editor = Member.objects \
                .filter(user=request.user) \
                .filter(role=Member.Roles.EDITOR)[0] \
                .exists()
        except IndexError:
            is_editor = False

        return render(request, 'jobs.html', {
            'is_company_editor': is_editor,
            'jobs': show_jobs,
            'page': page,
            'creation_form': create_job_form
        })
