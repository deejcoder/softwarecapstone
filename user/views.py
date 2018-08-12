from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
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

    def post(self, request, username):
        
        pic = request.FILES['profile_pic']
        fs = FileSystemStorage()

        # save the file as MEDIA_URL/{uuid}.{file format}
        file_ext = "." + pic.name.split('.')[-1]
        # generate a uuid for the new file, save it to the file system.
        file_uuid = uuid.uuid4()
        fs.save(str(file_uuid) + file_ext, pic)

        # update user's reference to this file & save the user
        request.user.avatar = file_uuid
        request.user.save()

        return render(request, 'user/user_profile.html', {
            'user': request.user,
            'success': "Your profile picture has successfully been changed."
        })




        