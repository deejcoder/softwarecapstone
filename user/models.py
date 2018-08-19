from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.uploadedfile import InMemoryUploadedFile
import uuid
from PIL import Image
import io

def upload_profile_image(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return "users/%s/%s" % (instance.id, filename)


class User(AbstractUser):
    # bio
    bio = models.TextField(max_length=500, blank=True)
    
    # avatar
    avatar_height = models.PositiveIntegerField(default = 0)
    avatar_width = models.PositiveIntegerField(default = 0)
    avatar = models.ImageField(
        upload_to=upload_profile_image,
        default='users/default/avatar.png',
        height_field='avatar_height',
        width_field='avatar_width'
    )
    
    # this overrides the save method for saving a User
    def save(self, **kwargs):
        super(User, self).save()

        # if the user has a new/old avatar
        if not self.avatar:
            return

        # if the image already meets the requirements, return
        if self.avatar_height == 200 and self.avatar_width == 200:
            return

        
        # otherwise resize the image
        image = Image.open(self.avatar.path)
        image = image.resize((200, 200), Image.ANTIALIAS)
        image.save(self.avatar.path)

        # update the image width & height columns
        self.avatar_height = 200
        self.avatar_width = 200
        super(User, self).save()

