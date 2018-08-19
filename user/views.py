from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import User
from django.contrib.auth import get_user_model
User = get_user_model()
import uuid
from django.contrib import messages
from django.http import HttpResponseRedirect

app_name = "user"

class Profile(View):

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

    """
    TODO: add a class declaring constant alert types, e.g class Alert.ALERT_ERROR
    """
    @method_decorator(login_required)
    def post(self, request, username):

        # get the user currently logged in
        current_user = request.user
        # get the user the profile belongs to
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

    def update_user_avatar(self, user : User, request):
        user.avatar = request.FILES['avatar']
        user.save()

        messages.success(request, "Your profile picture has successfully been updated.")




        
