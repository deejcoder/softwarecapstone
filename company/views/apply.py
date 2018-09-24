"""
Defines the views for handling company applications
"""
from django.shortcuts import redirect, render
from django.views import View
from ..forms import CompanyApplicationForm
from ..models import Member


# Temporary view for editing company profile
def edit_comp(request):
    dummy_form = CompanyApplicationForm()
    return render(request, 'company/edit_comp_profile.html', {'form':dummy_form})


# Rough view for comp_appform.html
class ApplyCompany(View):
    """Application form"""
    
    def get(self, request):
        """
        User wants to apply
        """
        form = CompanyApplicationForm()
        return render(request, 'company/apply.html', {'form': form})

    def post(self, request):
        """
        User submits the application form
        """
        form = CompanyApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=True)

            # make the user the owner of the company
            member = Member.objects.create(
                company=app,
                user=request.user,
                role=Member.Roles.OWNER
            )
            member.save()

        return redirect('/')
    
