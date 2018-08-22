from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from PIL import Image
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db.models.functions import Greatest


"""
==============================================================
Model: User
Defines a base User for the techpalmy website. Inherits from AbstractUser.
A user can be anyone with an account. Other systems expand on
this model.
==============================================================
"""
def upload_profile_image(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return "users/%s/%s" % (instance.id, filename)

class User(AbstractUser):

    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(
        upload_to=upload_profile_image,
        default='users/default/avatar.png' # if none, display default
    )

    """
    Overrides the saving of Users.
    This modifies a user's avatar e.g resizes it.
    """
    def save(self, **kwargs):
        super(User, self).save()

        # if the user has a new/old avatar
        if not self.avatar:
            return

        # otherwise resize the image
        image = Image.open(self.avatar.path)
        image = image.resize((200, 200), Image.ANTIALIAS)
        image.save(self.avatar.path)


    """
    Search all users against a given search term.
    returns: list of Users
    """
    @staticmethod
    def search_users(term : str) -> []:
        search_query = SearchQuery(term)
        search_vector = SearchVector('username') + SearchVector('first_name') + SearchVector('last_name')
        
        return User.objects.annotate(
            search=search_vector
        ).filter(
            search=search_query
        )


"""
==============================================================
Model: Consultant
Defines a Consultant, which extends the User model using a
one-to-one relationship. A consultant specializes in a particular
IT field.
==============================================================
"""
class Consultant(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    area_of_expertise = models.TextField(max_length=80)
    services_offered = models.TextField(max_length=300)
    work_phone = models.TextField(max_length=14, null=True, default=None)
    website = models.TextField(max_length=30, null=True, default=None)


    """
    Enables searching of consultants by,
    * area of expertise
    * services offered
    * their username
    * their first & last name.
    """
    @staticmethod
    def search_consultants(term : str):
        search_query = SearchQuery(term)
        search_vector = SearchVector('area_of_expertise') + SearchVector('services_offered')
        search_vector += SearchVector('user__username') + SearchVector('user__first_name') + SearchVector('user__last_name')

        return Consultant.objects.annotate(
            search=search_vector
        ).filter(
            search=search_query
        )
