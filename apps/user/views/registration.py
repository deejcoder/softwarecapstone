"""
Registration views: GET & POST (submitting form data)
"""

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
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
        Once the user has submitted the registration form,
        send them an email containing the verification code.
        """

        form = forms.UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)

            # send an email with verification code
            # a verification code is automatically generated when a User object is created.
            link = settings.SITE_DOMAIN + reverse('user:verify') + "?code=%d&username=%s" % (user.verify_code, username)
            msg_plain = render_to_string('emails/verification.txt', {'site': settings.SITE_DOMAIN, 'verify_link': link})
            user.email_user("TechPalmy: Verify your account", msg_plain)

            messages.success(request, "Please check your email and verify your account.")
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
        
        try:
            user = User.objects.get(username=username)

            if user.is_verified():
                messages.success(request, "Your account has already been verified.")

            elif str(user.verify_code) == verify_code:
                user.verify_code = 0
                user.save()

                messages.success(request, "Your account has successfully been verified! Please login to continue.")

                return HttpResponseRedirect(reverse('login'))
        except:
            pass

        return HttpResponseRedirect(reverse('index'))
