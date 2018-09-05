from django.shortcuts import render
from .forms import CompanyApplicationForm

# Create your views here.

#Temp view for company application form template

def company(request):
    label_list = ["IRD number", "Company name", "Street address", "Postal address", "Contact details", "Website", ]
    return render(request, 'company/comp_appform.html', {'list': label_list})


# Rough view for comp_appform.html
class ApplyCompany(View):
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
    
