from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.views.generic.base import TemplateView


class Index(TemplateView):
	template_name = 'index.html'
	def index(self, TemplateView):
		return render(request, 'index.html')