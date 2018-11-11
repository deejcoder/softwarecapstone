from datetime import datetime

from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db import models

from apps.entity.models import Entity


class Event(models.Model):

    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='event')
    title = models.CharField(max_length=80)
    date = models.DateField(default=None)
    time = models.TimeField(default=None)
    location = models.CharField(max_length=80)
    description = models.TextField(max_length=500*5.1)  # 5.1 = average word length

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return "{0} ({1})".format(self.title, self.pk)

    @classmethod
    def get_entity_events(cls, entity: Entity) -> []:
        """
        Returns a list of events associated with a particular entity (group or company)
        """
        return Event.objects.filter(entity=entity).select_related('entity')

    @classmethod
    def get_events(cls) -> []:
        """
        Returns a list of events which have not already 'happened'.
        """
        now = datetime.now()
        return Event.objects.filter(date__gte=now, time__gte=now)

    @classmethod
    def search_events(cls, term: str):
        """
        Searches companies or shows all if `term` is None
        :param term: the search string
        :return: list of companies
        """
        if term is None or term == "":
            result = cls.objects.all()

        else:
            search_query = SearchQuery(term)

            search_vector = SearchVector('title') + SearchVector('description')

            result = cls.objects.annotate(search=search_vector).filter(search=search_query)

        return result
