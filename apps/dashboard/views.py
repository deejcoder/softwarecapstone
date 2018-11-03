"""
Defines different views for the administrative dashboard.
TODO:
    - searching capabilities
    - consultant applications
    - POST request for approving & denying applications
"""

from apps.user.models import Consultant, User

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views import View

from apps.entity.models import Application
from apps.entity.models.company import Company


class Index(View):

    staff_member_required = True

    def get(self, request):
        return render(request, 'dashboard/index.html')


class Users(View):

    staff_member_required = True

    def get(self, request):
        users = User.objects.all()

        return render(request, 'dashboard/users.html', {
            'users': users
        })


class Consultants(View):

    staff_member_required = True

    def get(self, request):
        consultants = Consultant.objects.all()

        return render(request, 'dashboard/consultants.html', {
            'consultants': consultants
        })


class Companies(View):

    staff_member_required = True

    def get(self, request):
        companies = Company.objects.all()

        return render(request, 'dashboard/companies.html', {
            'companies': companies
        })


class CompanyApplications(View):

    staff_member_required = True
    
    def get(self, request):
        companies = Company.objects.filter(application__status="pending")

        return render(request, 'dashboard/companyapps.html', {
            'companies': companies
        })

    def post(self, request):
        """
        Approves or denies an application provided a
        cid & application status
        """

        try:
            cid = request.POST.get('cid')
            status = request.POST.get('status')
            company = Company.objects.get(id=cid)

        except (ObjectDoesNotExist, ValueError):
            return HttpResponseNotFound()

        if not request.user.is_staff():
            return HttpResponseNotFound()

        if status == "approve":
            company.application.approve(request.user, '')

        else:
            company.application.deny(request.user, '')

        messages.success(request, "You have approved the company application for: {0}".format(company.name))
        return render(request, 'dashboard/index.html')
