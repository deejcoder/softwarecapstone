"""
The User & Consultant models are defined here, with their corresponding
methods such as searching.
"""

import random
import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db import models
from overrides import overrides
from PIL import Image


def _upload_profile_image(instance, filename):
    """
    Helper function for User model.
    :return: file name with the format of 'uuid4.ext'
    """
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return "users/%s/%s" % (instance.id, filename)


def generate_random_code():
    """
    Generates a random verification code
    """
    return random.randint(10000000, 99999999)


class User(AbstractUser):
    """
    Model: User
    Extends Django's original User model.
    """

    bio = models.TextField(max_length=500, blank=True)
    verify_code = models.IntegerField(default=generate_random_code)
    avatar = models.ImageField(upload_to=_upload_profile_image, default=None, null=True)

    def is_verified(self) -> bool:
        """ Checks if user is verified """
        return True if self.verify_code == 0 else False

    def set_verified(self):
        """ Marks the user as verified """
        self.verify_code = 0

    @staticmethod
    def search_users(term: str) -> []:
        """
        Search all users.
        :param term: the search string
        :return: list of Users
        """
        search_query = SearchQuery(term)
        search_vector = (
            SearchVector('username') +
            SearchVector('first_name') +
            SearchVector('last_name')
        )

        return (
            User.objects.annotate(search=search_vector)
            .filter(search=search_query)
        )

    def is_consultant(self) -> bool:
        """
        Checks if a user is a consultant
        """
        if hasattr(self, 'consultant'):
            if self.consultant.status == 'approved':
                return True

        return False

    @property
    def avatar_url(self):
        """
        Returns the default avatar URL if
        the user does not have an avatar
        """
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        else:
            return "/media/users/default/avatar.png"

    @overrides
    def save(self, **kwargs):
        """
        Modifies a user's uploaded avatar after saving: resizing it
        """
        super(User, self).save()

        # if the user has a new/old avatar
        if not self.avatar:
            return

        try:
            # otherwise resize the image
            image = Image.open(self.avatar.path)
            image.thumbnail((200, 200), Image.ANTIALIAS)
            image.save(self.avatar.path)
        except:
            pass
