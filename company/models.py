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
    return "companies/%s/%s" % (instance.id, filename)


class Company(models.Model):
    """
    A company can also have profile pictures (logos)
    TODO: add regular expressions to restrict input
    """
   
    # The commented-out fields are ones that I tweaked for the form - the new fields are underneath the original ones
    # The industry and business choices variables can be changed whenever
    INDUSTRY_CHOICES = (
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('tertiary', 'Tertiary')
    )

    BUSINESS_CHOICES = (
        ('merc', 'Merchandising'),
        ('manu', 'Manufacturing'),
        ('serv', 'Services'),
        ('hybrid', 'Hybrid')
    )

    name = models.CharField(max_length=80)
    avatar = models.ImageField(
        upload_to=_upload_company_avatar,
        default=None,
        null=True
    )
    size = models.DecimalField(max_digits=5, decimal_places=0)
    # industry = models.CharField(max_length=30)
    industry = models.CharField(max_length=30, choices=INDUSTRY_CHOICES, default='primary')
    specialist_area = models.CharField(max_length=30)
    contact_phone = models.CharField(max_length=15)
    # contact_email = models.CharField(max_length=20)
    contact_email = models.EmailField(max_length=20)
    # website = models.CharField(max_length=20)
    website = models.URLField(max_length=20)
    # type_of_business = models.CharField(max_length=25)
    type_of_business = models.CharField(max_length=25, choices=BUSINESS_CHOICES, default='serv')
    address = models.CharField(max_length=80)
    ird_no = models.CharField(max_length=20)
    summer_students = models.BooleanField(default=False)

    def save(self, **kwargs):
        """
        Converts company avatar on save.
        """
        super(Company, self).save()

        if not self.avatar:
            return
        
        image = Image.open(self.avatar.path)
        image.thumbnail((200, 200), Image.ANTIALIAS)
        image.save(self.avatar.path)

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
    # permission roles
    class Roles:
        MEMBER = 'member'
        EDITOR = 'editor'
        OWNER = 'owner'

    PERMISSION_ROLES = (
        (Roles.MEMBER, 'Member'),
        (Roles.EDITOR, 'Editor'),
        (Roles.OWNER, 'Owner'),
    )

    # fields
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    role = models.CharField(max_length=30, choices=PERMISSION_ROLES)

    class Meta:
        unique_together = ('company', 'user')

    @classmethod
    def is_editor(cls, user: User, company: Company) -> bool:
        """
        An editor is an EDITOR or an OWNER.
        An editor can edit a company.
        :param user: the user to check
        :param company: the company the user belongs to
        :return: True if the user is administrator+ else False
        """
        member = cls.objects.filter(
            user=user,
            company=company
        )[0]

        if member.role in [cls.Roles.EDITOR, cls.Roles.OWNER]:
            return True
        return False

    @classmethod
    def get_members(cls, role: Roles) -> []:
        """
        :param role: Get members with the specific role
        :return: a list of Members (users)
        """
        member_ids = cls.objects.filter(
            role=role
        ).values_list('user', flat=True)
        return \
            User.objects.filter(id__in=member_ids)
