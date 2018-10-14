"""
Lists all groups, or filters/searches and lists the resulting groups.
"""

from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from entity.models.group import Group


class Listing(View):
    """
    Lists all groups
    """

    def get(self, request):

        try:
            search_term = request.GET.get('search')
            groups = Group.search_groups(search_term)

        except KeyError:
            groups = Group.search_groups(None)

        paginator = Paginator(groups, 6)
        page = request.GET.get('page')
        show_groups = paginator.get_page(page)

        return render(request, 'groups.html', {
            'groups': show_groups,
            'page': page
        })
