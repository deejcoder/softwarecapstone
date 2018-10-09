"""
Models which defines a company
"""
import uuid

from django.db import models
from djchoices import ChoiceItem, DjangoChoices
from PIL import Image


def _upload_company_avatar(group, filename):
    """
    Helper function for Company model
    :return: file name with uuid filename
    """
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    prefix = str()

    if group.category == Group.Category.Club:
        prefix = "clubs"
    else:
        prefix = "companies"

    return "groups/%s/%s" % (prefix, filename)


class Group(models.Model):

    # TYPE DEFINITIONS
    class Category(DjangoChoices):
        Club = ChoiceItem('club')
        Company = ChoiceItem('company')

    # FIELDS
    name = models.CharField(max_length=80)
    category = models.CharField(max_length=30, choices=Category.choices)
    avatar = models.ImageField(
        upload_to=_upload_company_avatar,
        default=None,
        null=True
    )

    # METHODS
    def save(self, **kwargs):
        """
        Manages saving of company avatar
        """
        super(Group, self).save()

        if not self.avatar:
            return

        image = Image.open(self.avatar.path)
        image.thumbnail((200, 200), Image.ANTIALIAS)
        image.save(self.avatar.path)

    @property
    def avatar_url(self):
        """
        Returns the default avatar URL if
        the company does not have an avatar
        """
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        else:
            return "/media/default/avatar.png"
