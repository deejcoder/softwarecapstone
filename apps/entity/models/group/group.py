"""
Models which defines a company
"""
from ckeditor.fields import RichTextField
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db import models

from apps.entity.models import Entity, Member


class Group(Entity):

    # FIELDS
    description = RichTextField(max_length=3000)  # 5.1 chars = average word length
    website = models.CharField(max_length=2056)

    def __str__(self):
        return "{0} ({1})".format(super().name, self.pk)

    def email_group(self, subject: str, msg: str):
        members = Member.get_members(self)
        for member in members:
            member.user.email_user(subject, msg)

    @classmethod
    def search_groups(cls, term: str):
        """
        Searches companies or shows all if `term` is None
        :param term: the search string
        :return: list of companies
        """
        if term is None or term == "":
            result = cls.objects.filter(application__status="approved")

        else:
            search_query = SearchQuery(term)
            search_vector = SearchVector('name') + \
                SearchVector('website')

            result = cls.objects.annotate(search=search_vector) \
                .filter(search=search_query) \
                .filter(application__status="approved")

        return result
