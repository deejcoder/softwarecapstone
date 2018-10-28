"""
Gives functionality to profiles, and allows users to view a profile.
Functionality includes editing of profiles.
"""

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from .. import forms
from ..models import User

User = get_user_model()


class Profile(View):
    """
    Allows someone to view a consultant's profile.
    This can later be extended for users when they
    actually have more functionality.
    """

    def get(self, request, username):
        """
        Allows a user to view a profile
        """

        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

        if not user.is_consultant() and user == request.user:
            return HttpResponseRedirect(reverse('user:user_profile_edit', args=[user.username]))
        elif not user.is_consultant():
            return HttpResponseNotFound()

        return render(request, 'profile/profile.html', {
            'viewing': user,
            'user': request.user,
            'is_owner': user == request.user,
        })


class EditProfile(View):
    """
    Renders the edit_profile page.
    """
    login_required = True

    def get(self, request, username):
        """
        User is editing profile...
        """

        if request.user.username != username:
            return HttpResponseNotFound()

        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

        user_form = forms.EditProfileForm(instance=user)
        avatar_form = forms.EditProfileAvatar()
        consult_form = forms.EditConsultantForm(instance=user.consultant)
        return render(request, 'profile/edit_profile.html', {
            'user': user,
            'is_owner': user == request.user,
            'user_form': user_form,
            'avatar_form': avatar_form,
            'consult_form': consult_form,
        })

    def post(self, request, username):
        """
        User updates profile.
        """

        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

        if username != request.user.username:
            return HttpResponseRedirect(request.path)

        self._update_user_avatar(user, request)
        self._update_info(user, request)

        return HttpResponseRedirect(request.path)

    def _update_user_avatar(self, user: User, request):
        """
        Helper function to allow a user to update their profile picture
        """
        form = forms.EditProfileAvatar(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()

            # add a message to the user's session
            messages.success(
                request,
                "Your profile picture has successfully been updated."
            )

    def _update_info(self, user: User, request):
        """
        Helper function for updating user/consultant information
        """
        user_form = forms.EditProfileForm(instance=user, data=request.POST)
        consult_form = forms.EditConsultantForm()

        # check if entered password matches current password
        if not user.check_password(user_form.data.get('current_password')):
            # if incorrect password
            user_form.add_error(
                'current_password',
                "You have provided an incorrect password"
            )

        else:

            if user_form.is_valid():

                user_form.save()

                # if user is a consultant, save consultant data
                if user.is_consultant():
                    consult_form = forms.EditConsultantForm(instance=user.consultant, data=request.POST)

                    if consult_form.is_valid():
                        consult_form.save()

                # user is logged out whenever their password changes since Django 1.7
                new_password = user_form.cleaned_data.get('password')
                auth = authenticate(username=user.username, password=new_password)
                login(request, auth)

                messages.success(
                    request,
                    "Your profile information has successfully been updated."
                )
                return
 
        return
