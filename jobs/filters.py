import django_filters
from .models import Job
from entity.models.company import Company


class JobFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Title', field_name='a_title')
    short_description = django_filters.CharFilter(lookup_expr='icontains', label='Description')
    company = django_filters.ModelChoiceFilter(queryset=Company.objects.all(), to_field_name='name')

    class Meta:
        model = Job
        fields = {'title', 'company', 'short_description'}
