import django_filters
from django import forms

from .models.company import Company


class FilterByIndustry(django_filters.FilterSet):
    specialist_area = django_filters.CharFilter(lookup_expr='icontains', label="Specialist area")

    class Meta:
        model = Company
        fields = ['industry', 'type_of_business', 'summer_students', 'specialist_area']
