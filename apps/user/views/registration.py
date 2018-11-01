"""
Registration views: GET & POST (submitting form data)
"""

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from apps.user.models import User

from .. import forms


class Register(View):

    def get(self, request):
        """
        User wants to register
        """
        form = forms.UserRegistrationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        """
        User has submitted registration form
        """

        form = forms.UserRegistrationForm(request.POST)

        # if form does not contain errors,
        if form.is_valid():

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            form.save()

            user = User.objects.get(username=username)

            # I'll change this tomorrow to something like this
            # https://stackoverflow.com/questions/2809547/creating-email-templates-with-django
            user.email_user(
                "TechPalmy: Verify your account",
                """
                Welcome to TechPalmy,
                To verify your account please click the link below.
                http://localhost:8000{0}?username={1}&code={2}
                """.format(reverse('user:verify'), user.username, user.verify_code),
                "g3itechpalmy@gmail.com"
            )

            messages.success(
                request,
                "Please check your email and verify your account."
            )
            return HttpResponseRedirect(reverse('index'))

        # if form has errors
        return render(request, 'registration/register.html', {'form': form})


class VerifyAccount(View):
    """
    Simply reads GET data, verifies the account
    if the verification code is correct, and then redirects
    them to the login page.
    """
    def get(self, request):

        verify_code = request.GET.get('code')
        username = request.GET.get('username')
        
        user = User.objects.get(username=username)

        if user.verify_code == 0:
            messages.success(
                request,
                "Your account has already been verified."
            )

        elif str(user.verify_code) == verify_code:
            user.verify_code = 0
            user.save()

            messages.success(
                request,
                "Your account has successfully been verified! Please login to continue."
            )

            return HttpResponseRedirect(reverse('login'))

        return HttpResponseRedirect(reverse('index'))
