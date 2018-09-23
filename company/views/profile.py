"""
Adds company profiles for users or guest to view
"""

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views import View

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

        return render(request, 'company/profile/profile.html', {
            'company': company_obj,
            'is_owner': False,
        })
