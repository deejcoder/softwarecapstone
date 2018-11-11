import django_filters
from .models import Event


class EventSearch(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Event
        fields = ['entity']
