"""
The views belonging to Consultant, this includes: listing/searching of
consultants.
"""

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views import View

from .. import forms
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
            search_term = request.GET.get('search')
            consultants = Consultant.search_consultants(search_term)

        # no
        except KeyError:
            # get all consultants
            consultants = Consultant.search_consultants(None)

        # divide consultants by five per page
        paginator = Paginator(consultants, 5)

        page = request.GET.get('page')
        show_consultants = paginator.get_page(page)

        return render(
            request,
            'consultant/consultants.html', 
            {'consultants': show_consultants}
        )


class Apply(View):
    """
    A page where users can apply to become consultants.
    """
    login_required = True

    def get(self, request):
        """
        User wants to apply
        """
        form = forms.ConsultantApplicationForm()
        return render(request, 'consultant/apply.html', {'form': form})

    def post(self, request):
        """
        User submits the application form
        """
        form = forms.ConsultantApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.save()

        return redirect('/consultants/')
