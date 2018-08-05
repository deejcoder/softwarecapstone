from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

app_label = "user"

class Profile(View):

    def get(self, request, username):
        """
        User wants to view their own or someone elses
        profile.
        """

        user = User.objects.get(username=username)
        
        return render(request, 'user/user_profile.html', {
            'username':username, # pass the username to the template
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_owner': request.user.username == username,
        })

    @login_required
    def post(self, request, *args, **kwargs):
        """
        A POST request can define if a user is updating their
        profile information. A user must be logged in to edit their
        details.
        """

        