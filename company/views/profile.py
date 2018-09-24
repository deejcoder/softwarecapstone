"""
Adds company profiles for users or guest to view
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from ..forms import EditCompanyForm
from ..models import Company


class Profile(View):
    """
    Lists all companies
    """

    def get(self, request, company):
        """
        User is editing profile...
        """

        try:
            company_obj = Company.objects.get(name=company)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

        form = EditCompanyForm()
        return render(request, 'company/profile/profile.html', {
            'company': company_obj,
            'is_owner': company_obj.is_owner(),
            'form': form,
        })

    @method_decorator(login_required)
    def post(self, request, company):

        # get the company object
        try:
            company = Company.objects.get(name=company)
        except ObjectDoesNotExist:
            return HttpResponseNotFound

        # is the user an editor (or owner)?
        if not company.is_editor(request.user):
            return HttpResponseRedirect(request.path)
        
        form = EditCompanyForm(instance=company, data=request.POST)

        # save company if valid
        if form.is_valid():
            form.save()
            messages.success(request, 'The company profile has successfully been updated.')
            form = EditCompanyForm()

        return render(request, 'company/profile/profile.html', {
            'company': company,
            'is_owner': company.is_owner(),
            'form': form
        })
