"""
Adds company profiles for users or guest to view
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View

from entity.forms import EditCompanyForm
from entity.models import Member
from entity.models.company import Company


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
            'is_owner': Member.is_owner(request.user, company_obj),
            'is_editor': Member.is_editor(request.user, company_obj),
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
            'is_owner': Member.is_owner(request.user, company),
            'is_editor': Member.is_editor(request.user, company),
            'form': form
        })


def company_remove(request, company):
    try:
        company_obj = Company.objects.get(name=company)
    except ObjectDoesNotExist:
        return HttpResponseNotFound

    if not Member.is_owner(request.user, company_obj):
        return HttpResponseRedirect(request.path)

    remove = get_object_or_404(Company, pk=company_obj.id)
    instance = Company.objects.get(id=company_obj.id)
    instance.delete()
    remove.delete()
    return redirect("/")    
 
