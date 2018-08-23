from django.shortcuts import render
from django.views import View

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from ..models import User
from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib import messages
from django.http import HttpResponseRedirect



class Profile(View):
    """
    Profile view adds functionality
    to users, allowing them to have profiles
    which others can view, and they can edit.
    """

    def get(self, request, username):
        """
        User wants to view their own or someone elses
        profile.
        """

        user = User.objects.get(username=username)
        
        return render(request, 'user/user_profile.html', {
            'user': user,
            'is_owner': user == request.user
        })


    @method_decorator(login_required)
    def post(self, request, username):
        """
        User wants to update profile.
        """

        # get the user currently logged in & who owns the profile being viewed
        current_user = request.user
        user = User.objects.get(username=username)

        if username != current_user.username:
            return HttpResponseRedirect(request.path)

        # updated avatar
        if request.FILES['avatar']:
            self.update_user_avatar(user, request)
        
        # updated other info
        else:
            pass

        return HttpResponseRedirect(request.path)


    # helper function for POST
    def update_user_avatar(self, user : User, request):
        user.avatar = request.FILES['avatar']
        user.save()

        # add a message to the user's session
        messages.success(
            request,
            "Your profile picture has successfully been updated."
        )




        
