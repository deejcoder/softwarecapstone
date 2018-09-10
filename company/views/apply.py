"""
Defines the views for handling company applications
"""
from django.shortcuts import redirect, render
from django.views import View
from ..forms import CompanyApplicationForm


# Rough view for comp_appform.html
class ApplyCompany(View):
    """Application form"""
    
    def get(self, request):
        """
        User wants to apply
        """
        form = CompanyApplicationForm()
        return render(request, 'company/comp_appform.html', {'form': form})

    def post(self, request):
        """
        User submits the application form
        """
        form = CompanyApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.save()

        return redirect('/company/')
    