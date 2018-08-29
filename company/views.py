from django.shortcuts import render

# Create your views here.

#Temp view for company application form template

def company(request):
    label_list = ["IRD number", "Company name", "Street address", "Postal address", "Contact details", "Website", ]
    return render(request, 'company/comp_appform.html', {'list': label_list})
