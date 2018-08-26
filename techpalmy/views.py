"""
This view file consists of general pages e.g homepage, contact-us.
"""
from django.shortcuts import render
from django.views.generic.base import TemplateView


class Index(TemplateView):
	"""
	Render homepage
	"""

	template_name = 'index.html'
	def index(self, TemplateView):
		return render(request, 'index.html')