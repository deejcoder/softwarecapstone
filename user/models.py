"""
The User & Consultant models are defined here, with their corresponding
methods such as searching.
"""

import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.core.validators import RegexValidator
from django.db import models
from djchoices import ChoiceItem, DjangoChoices
from PIL import Image
from ckeditor.fields import RichTextField


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
        default=None,
        null=True,
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

    def is_consultant(self) -> bool:
        """
        Checks if a user is a consultant
        """
        if hasattr(self, 'consultant'):
            return True
        else:
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


class Consultant(models.Model):
    """
    Model: Consultant
    There is a one-to-one relationship with the User model.
    """
    class ApprovalStatus(DjangoChoices):
        Pending = ChoiceItem("pending")
        Approved = ChoiceItem("approved")
        Denied = ChoiceItem("denied")

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    introduction = models.TextField(max_length=300)
    services_offered = RichTextField(max_length=3000)
    current_occupation = models.CharField(max_length=120, null=True, default=None)
    contact_phone = models.CharField(max_length=15, null=True, default=None, validators=[
        RegexValidator(regex='^[0-9]*$', message="A phone number can only contain numbers.")
    ])
    website = models.CharField(max_length=300, null=True, default=None)
    status = models.CharField(
        max_length=20,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.Pending
    )

    @classmethod
    def search_consultants(cls, term: str, status=ApprovalStatus.Approved):
        """
        Searches consultants or shows all if `term` is None
        :param term: the search string
        :param status: filter results by application status, None to show all.
        :return: list of consultants
        """
        if term is None or term == "":
            result = cls.objects.all()

        else:
            search_query = SearchQuery(term)
            search_vector = SearchVector('services_offered')

            search_vector += SearchVector('user__username') \
                + SearchVector('user__first_name') \
                + SearchVector('user__last_name')

            result = cls.objects.annotate(
                search=search_vector
            ).filter(
                search=search_query
            )

        if status is not None:
            return result.filter(status=status)
        else:
            return result
