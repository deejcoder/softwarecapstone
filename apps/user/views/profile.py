"""
Gives functionality to profiles, and allows users to view a profile.
Functionality includes editing of profiles.
"""

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.defaults import page_not_found

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
            return page_not_found(request, exception=ObjectDoesNotExist(), template_name='404.html')

        #if request.user.username != username:
        #    return page_not_found(request, exception=None, template_name='403.html')

        if user.is_consultant():
            return render(request, 'profile/profile.html', {
                'viewing': user,
                'user': request.user,
                'is_owner': user == request.user,
            })
        else:
            return redirect('user:user_profile_edit', username=user.username)


class EditProfile(View):
    """
    Renders the edit_profile page.
    """

    @method_decorator(login_required)
    def get(self, request, username):
        """
        User is editing profile...
        """

        if request.user.username != username:
            return page_not_found(request, exception=ObjectDoesNotExist(), template_name='403.html')

        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return page_not_found(request, exception=ObjectDoesNotExist(), template_name='404.html')

        user_form = forms.EditProfileForm(instance=user)

        if hasattr(user, 'consultant'):
            consult_form = forms.EditConsultantForm(instance=user.consultant)
        else:
            consult_form = None
            
        return render(request, 'profile/edit_profile.html', {
            'user': user,
            'is_owner': user == request.user,
            'user_form': user_form,
            'consult_form': consult_form,
        })

    @method_decorator(login_required)
    def post(self, request, username):
        """
        User updates profile.
        """

        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return page_not_found(request, exception=ObjectDoesNotExist(), template_name='404.html')

        if username != request.user.username:
            return page_not_found(request, exception=ObjectDoesNotExist(), template_name='403.html')

        self._update_info(user, request)
        return render(request, 'profile/edit_profile.html', {
            'user': user,
            'is_owner': user == request.user,
            'user_form': forms.EditProfileForm(request.POST, request.FILES or None, instance=user),
            'consult_form': forms.EditConsultantForm(request.POST, instance=user.consultant),
        })

    def _update_info(self, user: User, request):
        """
        Helper function for updating user/consultant information
        """
        user_form = forms.EditProfileForm(request.POST, request.FILES or None, instance=user)
        consult_form = forms.EditConsultantForm()

        # check if entered password matches current password
        if not user.check_password(user_form.data.get('current_password')):
            user_form.add_error('current_password', "You have provided an incorrect password")
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

                messages.success(request, "Your profile information has successfully been updated.")
                return
        return
