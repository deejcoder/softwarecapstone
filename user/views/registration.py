from django.shortcuts import render, redirect
from django.views import View

from ..models import Consultant
from .. import forms


class Register(View):

    def get(self, request):
        """
        User wants to register
        """
        form = forms.UserRegistrationForm()
        return render(request, 'registration/register.html', {'form': form})