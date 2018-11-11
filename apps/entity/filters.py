import django_filters
from .models.company import Company


class CompanyFilter(django_filters.FilterSet):
    class Meta:
        model = Company
        fields = ['industry', 'type_of_business', 'summer_students', ]