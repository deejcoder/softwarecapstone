"""
Gives functionality to profiles, and allows users to view a profile.
Functionality includes editing of profiles.
"""

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.utils.decorators import method_decorator
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

        return render(request, 'user/profile/profile.html', {
            'viewing': user,
            'user': request.user,
            'is_owner': user == request.user
        })


class EditProfile(View):
    """
    Renders the edit_profile page.
    """

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

        form = forms.EditProfileForm()
        return render(request, 'user/profile/edit_profile.html', {
            'user': user,
            'is_owner': user == request.user,
            'form': form,
        })

    @method_decorator(login_required)
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

        # updated avatar
        try:
            request.FILES['avatar']
            self._update_user_avatar(user, request)

        # updated other info
        except KeyError:
            # todo: implement user profile form in forms.py
            self._update_user_info(user, request)

        return HttpResponseRedirect(request.path)

    def _update_user_avatar(self, user: User, request):
        """
        Helper function to allow a user to update their profile picture
        """
        user.avatar = request.FILES['avatar']
        user.save()

        # add a message to the user's session
        messages.success(
            request,
            "Your profile picture has successfully been updated."
        )

    def _update_user_info(self, user: User, request):
        """
        Helper function for updating user information
        """
        form = forms.EditProfileForm(request.POST)
        # check if entered password matches current password
        if not authenticate(
                username=user.username,
                password=form.fields['current_password']
        ):
            # if incorrect password
            form.add_error(
                'current_password',
                "You have provided an incorrect password"
            )
            return render_to_response(
                request.path,
                {'form': form}
            )

        # else save
        user.save()

        messages.success(
            request,
            "Your profile information has successfully been updated."
        )
