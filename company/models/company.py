"""
Models which defines a company
"""
import uuid

from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db import models
from djchoices import ChoiceItem, DjangoChoices
from PIL import Image


def _upload_company_avatar(company, filename):
    """
    Helper function for Company model
    :return: file name with uuid filename
    """
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return "companies/%s/%s" % (company.id, filename)


class Company(models.Model):
    """
    A company can also have profile pictures (logos)
    TODO: add regular expressions to restrict input
    """

    # TYPE DEFINITIONS
    class IndustryType(DjangoChoices):
        Primary = ChoiceItem('primary')
        Secondary = ChoiceItem('secondary')
        Tertiary = ChoiceItem('tertiary')

    class BusinessType(DjangoChoices):
        Merchandising = ChoiceItem('merchandising')
        Manufacturing = ChoiceItem('manufacturing')
        Services = ChoiceItem('services')
        Hybrid = ChoiceItem('hybrid')

    class StatusType(DjangoChoices):
        Pending = ChoiceItem('pending')
        Approved = ChoiceItem('approved')
        Denied = ChoiceItem('denied')

    # FIELDS
    name = models.CharField(max_length=80)
    avatar = models.ImageField(
        upload_to=_upload_company_avatar,
        default=None,
        null=True
    )
    size = models.DecimalField(max_digits=5, decimal_places=0)
    industry = models.CharField(
        max_length=30,
        choices=IndustryType.choices,
        default=IndustryType.Primary
    )
    specialist_area = models.CharField(max_length=30)
    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField(max_length=20)
    website = models.URLField(max_length=20)
    type_of_business = models.CharField(
        max_length=25,
        choices=BusinessType.choices,
        default=BusinessType.Services
    )
    address = models.CharField(max_length=80)
    summer_students = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=StatusType.choices,
        default=StatusType.Pending
    )

    # METHODS
    def save(self, **kwargs):
        """
        Manages saving of company avatar
        """
        super(Company, self).save()

        if not self.avatar:
            return

        image = Image.open(self.avatar.path)
        image.thumbnail((200, 200), Image.ANTIALIAS)
        image.save(self.avatar.path)

    @classmethod
    def search_companies(cls, term: str) -> []:
        """
        Search all companies
        :return: list of companies
        """
        search_query = SearchQuery(term)
        search_vector = SearchVector('company_name') \
            + SearchVector('industry')

        return cls.objects.annotate(
            search=search_vector
        ).filter(
            search=search_query
        )
