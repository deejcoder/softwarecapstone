from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator

from ..models import Consultant

class Listing(View):

    def get(self, request):

        # get all consultants
        consultants = Consultant.objects.all()

        # divide consultants by five per page
        paginator = Paginator(consultants, 5)
        # get current page
        page = request.GET.get('page')
        show_consultants = paginator.get_page(page)

        return render(
            request, 
            'user/consultants.html', 
            {'consultants' : show_consultants}
        )