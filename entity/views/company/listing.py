"""
Lists all companies, or filters/searches and lists the resulting companies.
"""

from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from entity.models.company import Company
from user.models import Consultant


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
            'companies': show_businesses,
            'page': page
        })
