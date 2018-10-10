"""
Models which defines a company
"""
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db import models
from entity.models import Entity


class Group(Entity):

    # FIELDS
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    website = models.CharField(max_length=100)

    @classmethod
    def search_groups(cls, term: str):
        """
        Searches companies or shows all if `term` is None
        :param term: the search string
        :return: list of companies
        """
        if term is None:
            result = cls.objects.filter(application__status="accepted")

        else:
            search_query = SearchQuery(term)
            search_vector = SearchVector('name') + \
                SearchVector('website')

            result = cls.objects.annotate(search=search_vector) \
                .filter(search=search_query) \
                .filter(application__status="accepted")

        return result
