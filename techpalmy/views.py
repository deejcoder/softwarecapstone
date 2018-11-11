"""
This view file consists of general pages e.g homepage, contact-us.
"""
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView, View
from .forms import ContactForm


class Index(TemplateView):
    """
    Render homepage
    """

    template_name = 'index.html'

    def index(self, request):
        return render(request, 'index.html')

    
class About(TemplateView):

    template_name = 'about.html'

    def index(self, request):
        return render(request, 'about.html')


class Contact(View):

    def get(self, request):
        form = ContactForm()
        return render(request, 'contact.html', {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            return redirect("/")
