"""
Models which defines a company
"""
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db import models
from djchoices import ChoiceItem, DjangoChoices
from entity.models import Entity


class Company(Entity):
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

    # FIELDS
    name = models.CharField(max_length=80)
    size = models.DecimalField(max_digits=5, decimal_places=0)
    industry = models.CharField(max_length=30, choices=IndustryType.choices, default=IndustryType.Primary)
    specialist_area = models.CharField(max_length=30)
    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField(max_length=20)
    website = models.URLField(max_length=20)
    type_of_business = models.CharField(max_length=25, choices=BusinessType.choices, default=BusinessType.Services)
    address = models.CharField(max_length=80)
    summer_students = models.BooleanField(default=False)

    @classmethod
    def search_companies(cls, term: str):
        """
        Searches companies or shows all if `term` is None
        :param term: the search string
        :return: list of companies
        """
        if term is None:
            result = cls.objects.filter(application__status="pending")

        else:
            search_query = SearchQuery(term)
            search_vector = SearchVector('name')

            search_vector += SearchVector('industry') \
                + SearchVector('specialist_area')

            result = cls.objects.annotate(search=search_vector) \
                .filter(search=search_query) \
                .filter(application__status="pending")  # change to accepted

        return result
