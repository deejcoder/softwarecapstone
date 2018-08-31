"""
Models which defines a company
"""
import uuid
from user.models import User

from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db import models
from PIL import Image
from modeltools.enums import Enum


def _upload_company_avatar(instance, filename):
    """
    Helper function for Company model
    :return: file name with uuid filename
    """
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return "companies/%s/%s" % (instance.id, filename)


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
    Roles = Enum(
        MEMBER=('member', 'Member'),
        ADMIN=('admin', 'Administrator'),
        OWNER=('owner', 'Owner')
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=30,
        choices=Roles.choices()
    )

    class Meta:
        # add a unique constraint for company & user
        unique_together = ('company', 'user')

    @staticmethod
    def is_administrator(user: User, company: Company) -> bool:
        """
        :param user: the user to check
        :param company: the company the user belongs to
        :return: True if the user is administrator+ else False
        """
        member = CompanyMembers.objects.filter(
            user=user,
            company=company
        )[0]

        if member.role in [CompanyMembers.Roles.OWNER, CompanyMembers.Roles.ADMIN]:
            return True
        return False


    @classmethod
    def get_members(cls) -> []:
        """
        :return: a list of Members (users)
        """
        member_ids = cls.objects.filter(
            role=cls.Roles.MEMBER
        ).values_list('user', flat=True)
        return \
            User.objects.filter(id__in=member_ids)

    @classmethod
    def get_administrators(cls) -> []:
        """
        :return: a list of administrators (Users)
        """

        admin_ids = cls.objects.filter(
            role=cls.Roles.ADMIN
        ).values_list('user', flat=True)
        return \
            User.objects.filter(id__in=admin_ids)

    @classmethod
    def get_owners(cls) -> []:
        """
        :return: a list of owners (Users)
        """

        owner_ids = cls.objects.filter(
                role=cls.Roles.OWNER
            ).values_list('user', flat=True)
        return \
            User.objects.filter(id__in=owner_ids)
