"""
Models which defines a company
"""
import uuid
from user.models import User

from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db import models
from PIL import Image


def _upload_company_avatar(instance, filename):
    """
    Helper function for Company model
    :return: file name with uuid filename
    """
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return "users/%s/%s" % (instance.id, filename)


class Company(models.Model):
    """
    A company can also have profile pictures (logos)
    TODO: add regular expressions to restrict input
    """

    company_name = models.CharField(max_length=80)
    company_avatar = models.ImageField(
        upload_to=_upload_company_avatar,
        default=None,
        null=True
    )
    company_size = models.DecimalField(max_digits=5, decimal_places=0)
    industry = models.CharField(max_length=30)
    specialist_area = models.CharField(max_length=30)
    contact_phone = models.CharField(max_length=15)
    contact_email = models.CharField(max_length=20)
    website = models.CharField(max_length=20)
    type_of_business = models.CharField(max_length=25)
    address = models.CharField(max_length=80)
    summer_students = models.BooleanField(default=False)

    def save(self, **kwargs):
        """
        Converts company avatar on save.
        """
        super(Company, self).save()

        if not self.company_avatar:
            return
        
        image = Image.open(self.company_avatar.path)
        image.thumbnail((200, 200), Image.ANTIALIAS)
        image.save(self.company_avatar.path)

    @staticmethod
    def search_companies(term: str) -> []:
        """
        Search all companies
        :return: list of companies
        """
        search_query = SearchQuery(term)
        search_vector = SearchVector('company_name') \
            + SearchVector('industry')

        return Company.objects.annotate(
            search=search_vector
        ).filter(
            search=search_query
        )


class CompanyMembers(models.Model):
    """
    A company has many members (users) with different permissions (roles).
    """

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # there may be multiple owners
    ROLE_CHOICES = (
        ("member", "Member"),
        ("administrator", "Administrator"),
        ("owner", "Owner")
    )
    role = models.CharField(max_length=12, choices=ROLE_CHOICES)

    @staticmethod
    def get_members() -> []:
        """
        :return: a list of Members (users)
        """
        return \
            Company.objects.filter(
                'role=member'
            ).values_list('user', flat=True)

    @staticmethod
    def get_administrators() -> []:
        """
        :return: a list of administrators (Users)
        """

        return \
            Company.objects.filter(
                'role=administrator'
            ).values_list('user', flat=True)

    @staticmethod
    def get_owners() -> []:
        """
        :return: a list of owners (Users)
        """

        return \
            Company.objects.filter(
                'role=owner'
            ).values_list('user', flat=True)

