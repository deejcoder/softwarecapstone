"""
Registration views: GET & POST (submitting form data)
"""
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.urls import reverse
from django.views import View

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
            # create the new user
            form.save()

            # log the user in automatically
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            messages.success(
                request,
                "Your account has now been registered. Welcome to techpalmy!"
            )

            # redirect user to their profile
            return HttpResponseRedirect(
                reverse(
                    'user:user_profile',
                    kwargs={'username': username}
                )
            )

        # if form has errors
        else:
            print("A message in there")
            return render_to_response(
                'registration/register.html',
                {'form': form,
				'user' : request.user
            }
            )
