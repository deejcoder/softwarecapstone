"""
Lists all companies, or filters/searches and lists the resulting companies.
"""

from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from apps.entity.models.company import Company
from apps.user.models import Consultant
from apps.entity.models import Member


class Listing(View):
    """
    Lists all companies
    """

    def get(self, request):

        try:
            search_term = request.GET.get('search')

            # get all results from companies & consultants
            companies = Company.search_companies(search_term)

        except KeyError:
            # get all companies and consultants
            companies = Company.search_companies(None)

        paginator = Paginator(companies, 8)
        page = request.GET.get('page')
        show_businesses = paginator.get_page(page)

        return render(request, 'companies.html', {
            'company': Member.get_user_company(request.user),
            'show_sidepane': True,
            'companies': show_businesses,
            'page': page
        })
