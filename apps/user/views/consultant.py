"""
The views belonging to Consultant, this includes: listing/searching of
consultants.
"""

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.defaults import page_not_found

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

    @method_decorator(login_required)
    def get(self, request):
        """
        User wants to apply
        """

        user = request.user
        if user.is_consultant():
            return page_not_found(request, exception=None, template_name='403.html')

        form = forms.ConsultantApplicationForm()
        return render(request, 'consultant/apply.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        """
        User submits the application form
        """
        user = request.user
        if user.is_consultant():
            return page_not_found(request, exception=None, template_name='403.html')

        form = forms.ConsultantApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = user
            app.save()

        return redirect('/consultants/')
