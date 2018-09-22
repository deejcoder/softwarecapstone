"""
Lists all companies, or filters/searches and lists the resulting companies.
"""

from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from ..models import Company


class Listing(View):
    """
    Lists all companies
    """

    def get(self, request):

        try:
            search_term = request.GET.get('page')
            companies = Company.search_companies(search_term)

        except KeyError:
            companies = Company.search_companies(None)

        paginator = Paginator(companies, 5)
        page = request.GET.get('page')
        show_companies = paginator.get_page(page)

        return render(
            request,
            'companies.html',
            {'companies': show_companies}
        )
