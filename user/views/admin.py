"""
Defines different views for the administrative dashboard.
TODO:
    - searching capabilities
    - consultant applications
    - POST request for approving & denying applications
"""

from django.shortcuts import render
from django.views import View

from ..models import Consultant, User
from company.models import Company, CompanyApplication

class Users(View):

    def get(self, request):
        users = User.objects.all()

        return render(request, 'admin/dashboard.html', {
            'users': users
        })

class Consultants(View):

    def get(self, request):
        consultants = Consultant.search_consultants(None)

        return render(request, 'admin/dashboard.html', {
            'consultants': consultants
        })

class Companies(View):

    def get(self, request):
        companies = Company.search_companies(None)

        return render(request, 'admin/dashboard.html', {
            'companies': companies
        })

class CompanyApplications(View):

    def get(self, request):
        applications = CompanyApplication.objects.all()

        return render(request, 'admin/dashboard.html', {
            'applications': applications
        })
