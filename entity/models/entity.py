"""
Models which defines a company
"""
import uuid

from django.db import models
from django.apps import apps
from PIL import Image


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
    avatar = models.ImageField(
        upload_to=_upload_company_avatar,
        default=None,
        null=True
    )

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
