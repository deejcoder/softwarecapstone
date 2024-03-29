import datetime

from django.contrib.postgres.search import SearchQuery, SearchVector
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField

from apps.entity.models.company import Company


class Job(models.Model):

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=50)
    location = models.CharField(max_length=50)  # 30 is too short!
    short_description = models.TextField(max_length=150, default="")
    description = RichTextField(max_length=3500)  # average word length=5.1
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15, validators=[
        RegexValidator(regex='^[0-9]*$', message="A phone number can only contain numbers.")
    ])
    date_posted = models.DateTimeField(default=timezone.now())
    expiry = models.DateTimeField(default=(timezone.now()+datetime.timedelta(days=14)))
    external_link = models.CharField(blank=True, max_length=2072, default=None)  # IE has URL max length=2083 (reduced by 11 for no https://www. case)

    @classmethod
    def search_jobs(cls, term: str):
        """
        Searches jobs against a given search term. If term is None, show all.
        """
        if term is None or term == "":
            result = cls.objects.all()
        
        else:
            search_query = SearchQuery(term)

            search_vector = SearchVector('title') \
                + SearchVector('description')
        
            result = cls.objects.annotate(search=search_vector) \
                .filter(search=search_query)

        return result

    @classmethod
    def get_recent_jobs(company: Company):
        """
        Returns the four most recent job postings for a company
        """
        jobs = Job.objects \
            .filter(company=company) \
            .filter(expiry__lt=timezone.now()) \
            .order_by('-date_posted')[:4]

        return jobs
