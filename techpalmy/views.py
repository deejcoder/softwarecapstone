"""
This view file consists of general pages e.g homepage, contact-us.
"""
from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from django import forms
from .forms import ContactForm


class Index(TemplateView):
    """
    Render homepage
    """

    template_name = 'index.html'
    def index(self, TemplateView):
        return render(request, 'index.html')

    
class About(TemplateView):

    template_name = 'about.html'
    def index(self, TemplateView):
        return render(request, 'about.html')


def contact_form(request):
    form = ContactForm()
    return render(request, 'contact.html', {'form': form})

