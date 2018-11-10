"""
Lists all companies, or filters/searches and lists the resulting companies.
"""

from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from apps.entity.models.company import Company
from apps.user.models import Consultant
from apps.entity.models import Member
from apps.entity.filters import FilterByIndustry


class Listing(View):
    """
    Lists all companies
    """

    def get(self, request):

        company_list = Company.objects.all()
        company_filter = FilterByIndustry(request.GET, queryset=company_list)
        results = company_filter.qs

        paginator = Paginator(results, 8)
        page = request.GET.get('page')
        show_businesses = paginator.get_page(page)

        return render(request, 'companies.html', {
            'company': Member.get_user_company(request.user),
            'show_sidepane': True,
            'companies': show_businesses,
            'page': page,
            'filter': company_filter,
        })
