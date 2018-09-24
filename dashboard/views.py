"""
Defines different views for the administrative dashboard.
TODO:
    - searching capabilities
    - consultant applications
    - POST request for approving & denying applications
"""

from django.shortcuts import render
from django.views import View

from user.models import Consultant, User
from company.models import Company, CompanyApplication


class Index(View):

    def get(self, request):
        return render(request, 'dashboard/index.html')


class Users(View):

    def get(self, request):
        users = User.objects.all()

        return render(request, 'dashboard/users.html', {
            'users': users
        })


class Consultants(View):

    def get(self, request):
        consultants = Consultant.objects.all()

        return render(request, 'dashboard/consultants.html', {
            'consultants': consultants
        })


class Companies(View):

    def get(self, request):
        companies = Company.objects.all()

        return render(request, 'dashboard/companies.html', {
            'companies': companies
        })


class CompanyApplications(View):

    def get(self, request):
        companies = Company.objects.filter(application__status="pending")

        return render(request, 'dashboard/company_apps.html', {
            'companies': companies
        })
