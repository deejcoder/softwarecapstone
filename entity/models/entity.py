"""
Models which defines a company
"""
import uuid

from django.apps import apps
from django.core.validators import RegexValidator
from django.db import models
from PIL import Image
from django.core.exceptions import ValidationError


def _upload_company_avatar(entity, filename):
    """
    Helper function for Company model
    :return: file name with uuid filename
    """
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)

    return "entities/%s" % (filename)


class Entity(models.Model):

    # FIELDS
    name = models.CharField(max_length=80, validators=[
        RegexValidator(regex='^[\w|\W]*$', message="Your name can only include characters 0-9, A-Z or a-z.")
    ])
    introduction = models.TextField(max_length=300)
    avatar = models.ImageField(
        upload_to=_upload_company_avatar,
        default=None,
        null=True,
    )

    def __str__(self):
        return "{0} ({1})".format(self.name, self.pk)

    def create_application(self):
        application = apps.get_model('entity', 'Application')
        application.objects.create(entity=self)

    # METHODS
    def save(self, *args, **kwargs):
        """
        Manages saving of company avatar
        """
        # determine if the entity was just created
        created = self.pk is None
        super(Entity, self).save(*args, **kwargs)
        

        if created:
            self.create_application()

        # Uploaded an avatar?
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
