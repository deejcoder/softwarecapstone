"""
The User & Consultant models are defined here, with their corresponding
methods such as searching.
"""

import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db import models
from PIL import Image


def _upload_profile_image(instance, filename):
    """
    Helper function for User model.
    :return: file name with the format of 'uuid4.ext'
    """
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return "users/%s/%s" % (instance.id, filename)


class User(AbstractUser):
    """
    Model: User
    Inherits from AbstractUser, extending it.
    """

    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(
        upload_to=_upload_profile_image,
        default='users/default/avatar.png'  # if none, display default
    )

    @property
    def full_name(self):
        """
        :return: the full name of a User e.g Bob McGrant
        """
        return "%s %s" % (self.first_name, self.last_name)

    def save(self, **kwargs):
        """
        Overrides the saving of Users.
        This modifies a user's avatar e.g resizes it.
        """
        super(User, self).save()

        # if the user has a new/old avatar
        if not self.avatar:
            return

        # otherwise resize the image
        image = Image.open(self.avatar.path)
        image.thumbnail((200, 200), Image.ANTIALIAS)
        image.save(self.avatar.path)

    @staticmethod
    def search_users(term: str) -> []:
        """
        Search all users.
        :param term: the search string
        :return: list of Users
        """
        search_query = SearchQuery(term)
        search_vector = SearchVector('username') \
            + SearchVector('first_name') \
            + SearchVector('last_name')

        return User.objects.annotate(
            search=search_vector
        ).filter(
            search=search_query
        )

"""
Certifications is probably another field that should be added to the consultants model. (<-- multivaluefield?)
Area of expertise doesn't need to be a text-field - a char-field will suffice for now.
Services_offered can potentially expand on area_of_expertise.
"""

class Consultant(models.Model):
    """
    Model: Consultant
    There is a one-to-one relationship with the User model.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    area_of_expertise = models.TextField(max_length=80)
    services_offered = models.TextField(max_length=300)
    work_phone = models.CharField(max_length=14, null=True, default=None)
    website = models.CharField(max_length=30, null=True, default=None)
    status = models.CharField(max_length=20, default="Pending")

    @staticmethod
    def search_consultants(term: str):
        """
        Searches consultants
        :param term: the search string
        :return: list of consultants
        """
        search_query = SearchQuery(term)
        search_vector = SearchVector('area_of_expertise') \
            + SearchVector('services_offered')

        search_vector += SearchVector('user__username') \
            + SearchVector('user__first_name') \
            + SearchVector('user__last_name')

        return Consultant.objects.annotate(
            search=search_vector
        ).filter(
            search=search_query
        )
