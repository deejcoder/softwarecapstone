"""
This view file consists of general pages e.g homepage, contact-us.
"""
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django import forms


class Index(TemplateView):
	"""
	Render homepage
	"""

	template_name = 'index.html'
	def index(self, TemplateView):
		return render(request, 'index.html')

class Dashboard(TemplateView):
	"""
	Render dashboard homepage
	"""

	template_name = "dashboard/index.html"
	def index(self, TemplateView):
		return render(request, 'dashboard/index.html')
	
class About(View):
    def index(self):
        return render(request, 'abour.html')


def contact_form(request):
    form = ContactForm()
    return render(request, 'contact.html', {'form': form})
