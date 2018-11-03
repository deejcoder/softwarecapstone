"""
The User & Consultant models are defined here, with their corresponding
methods such as searching.
"""

from ckeditor.fields import RichTextField
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.core.validators import RegexValidator
from django.db import models
from djchoices import ChoiceItem, DjangoChoices

from apps.user.models import User


class Consultant(models.Model):
    """
    Model: Consultant
    There is a one-to-one relationship with the User model.
    """
    class ApprovalStatus(DjangoChoices):
        Pending = ChoiceItem("pending")
        Approved = ChoiceItem("approved")
        Denied = ChoiceItem("denied")

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    introduction = models.TextField(max_length=300)
    services_offered = RichTextField(max_length=3000)
    current_occupation = models.CharField(max_length=120, null=True, default=None)
    area_of_expertise = models.CharField(max_length=120, null=True, default=None)
    contact_phone = models.CharField(max_length=15, null=True, default=None, validators=[
        RegexValidator(regex='^[0-9]*$', message="A phone number can only contain numbers.")
    ])
    contact_email = models.EmailField(max_length=30, null=True, default=None)
    website = models.CharField(max_length=300, null=True, default=None)
    status = models.CharField(max_length=20, choices=ApprovalStatus.choices, default=ApprovalStatus.Pending)

    @classmethod
    def search_consultants(cls, term: str, status=ApprovalStatus.Approved):
        """
        Searches consultants or shows all if `term` is None
        :param term: the search string
        :param status: filter results by application status, None to show all.
        :return: list of consultants
        """
        if term is None or term == "":
            result = cls.objects.all()

        else:
            search_query = SearchQuery(term)
            search_vector = SearchVector('services_offered')

            search_vector += SearchVector('user__username') \
                + SearchVector('user__first_name') \
                + SearchVector('user__last_name')

            result = cls.objects.annotate(
                search=search_vector
            ).filter(
                search=search_query
            )

        if status is not None:
            return result.filter(status=status)
        else:
            return result
