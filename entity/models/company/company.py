"""
Models which defines a company
"""
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.core.validators import RegexValidator
from django.db import models
from djchoices import ChoiceItem, DjangoChoices

from entity.models import Entity


class Company(Entity):

    class IndustryType(DjangoChoices):
        Primary = ChoiceItem('primary')
        Secondary = ChoiceItem('secondary')
        Tertiary = ChoiceItem('tertiary')

    class BusinessType(DjangoChoices):
        Merchandising = ChoiceItem('merchandising')
        Manufacturing = ChoiceItem('manufacturing')
        Services = ChoiceItem('services')
        Hybrid = ChoiceItem('hybrid')

    size = models.DecimalField(max_digits=5, decimal_places=0)
    industry = models.CharField(max_length=30, choices=IndustryType.choices, default=IndustryType.Primary)
    specialist_area = models.CharField(max_length=(1530))
    contact_phone = models.CharField(max_length=15, validators=[
        RegexValidator(regex='^[0-9]*$', message="A phone number can only contain numbers.")
    ])
    contact_email = models.EmailField()
    website = models.URLField(max_length=300)
    type_of_business = models.CharField(max_length=25, choices=BusinessType.choices, default=BusinessType.Services)
    address = models.CharField(max_length=200, null=True, default=None)
    summer_students = models.BooleanField(default=False)

    def __str__(self):
        return "{0} ({1})".format(super().name, self.pk)

    @classmethod
    def search_companies(cls, term: str):
        """
        Searches companies or shows all if `term` is None
        :param term: the search string
        :return: list of companies
        """
        if term is None or term == "":
            result = cls.objects.filter(application__status="approved")

        else:
            search_query = SearchQuery(term)

            search_vector = SearchVector('name') \
                + SearchVector('industry') \
                + SearchVector('specialist_area')

            result = cls.objects.annotate(search=search_vector) \
                .filter(search=search_query) \
                .filter(application__status="approved")  # change to accepted

        return result
