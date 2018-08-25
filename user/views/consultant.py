"""
The views belonging to Consultant, this includes: listing/searching of
consultants.
"""

from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from ..models import Consultant


class Listing(View):
    """
    Lists all consultants
    """

    def get(self, request):
        """
        Lists the consultants for the current page, and applies the search
        filter if it exists.
        """

        # search? yes
        try:
            search_term = request.GET['search']
            consultants = Consultant.search_consultants(search_term)

        # no
        except KeyError:
            # get all consultants
            consultants = Consultant.objects.all()

        # divide consultants by five per page
        paginator = Paginator(consultants, 5)

        page = request.GET.get('page')
        show_consultants = paginator.get_page(page)

        return render(
            request,
            'user/consultants.html', 
            {'consultants': show_consultants}
        )
