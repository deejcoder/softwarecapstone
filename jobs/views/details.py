"""
Lists all jobs, allows companies to add new jobs
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from entity.models.members import Member

from ..forms import EditJobForm
from ..models import Job


class Detail(View):

    def get(self, request, job_title, job_id):

        try: 
            job = Job.objects.get(pk=job_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

        return render(request, 'jobs/details.html', {
            'job': job,
        })

    
class EditDetails(View):
    login_required = True

    def get(self, request, job_title, job_id):
        try:
            job = Job.objects.get(pk=job_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

        form = EditJobForm(data=request.GET)
        company_obj = job.company

        return render(request, 'jobs/edit_job.html', {
            'job': job,
            'is_owner': Member.is_owner(request.user, company_obj),
            'is_editor': Member.is_editor(request.user, company_obj),
            'form': form,
        })


    def post(self, request, job_title, job_id):
        try:
            job_obj = Job.objects.get(pk=job_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

        form = EditJobForm(instamce=job_obj, data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'The job listing has successfully been updated.')
            form = EditJobForm()

        return HttpResponseRedirect(reverse('jobs:job_listing'))


@login_required
def remove_job(request, job_title, job_id):
    try:
        job_obj = Job.objects.get(pk=job_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound

    entity_obj = Job.objects.get(title=job_title).company

    if not Member.is_owner(request.user, entity_obj):
        return HttpResponseRedirect(request.path)

    remove = get_object_or_404(Job, pk=job_obj.id)
    instance = Job.objects.get(id=job_obj.id)
    instance.delete()
    remove.delete()
    return redirect("/")
