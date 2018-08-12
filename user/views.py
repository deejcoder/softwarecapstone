from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
import uuid
from django.core.files.storage import FileSystemStorage

app_name = "user"

class Profile(View):

    def get(self, request, username):
        """
        User wants to view their own or someone elses
        profile.
        """

        user = User.objects.get(username=username)
        
        return render(request, 'user/user_profile.html', {
            'user': user
        })

    @method_decorator(login_required)
    def post(self, request, username):

        logged_user = request.user
        # current profile being viewed
        current_user = User.objects.get(username=username)

        # if the user does not own this profile
        if logged_user.username is not username:
            return render(request, 'user/user_profile.html', {
                'user': current_user,
                'success': "You are not the owner of this profile."

            })
        
        pic = request.FILES['profile_pic']
        fs = FileSystemStorage()

        # save the file as MEDIA_URL/{uuid}.{file format}
        file_ext = "." + pic.name.split('.')[-1]
        # generate a uuid for the new file, save it to the file system.
        file_uuid = uuid.uuid4()
        fs.save(str(file_uuid) + file_ext, pic)

        # update user's reference to this file & save the user
        user.avatar = file_uuid
        user.save()

        return render(request, 'user/user_profile.html', {
            'user': current_user,
            'success': "Your profile picture has successfully been changed."
        })




        