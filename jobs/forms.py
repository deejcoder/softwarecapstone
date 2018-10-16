import pickle

from django import forms
from django.forms import ModelForm

from jobs.models import Job


class JobCreationForm(ModelForm):

    class Meta:
        model = Job

        fields = [
            'company',
            'title',
            'description',
            'location',
            'contact_email',
            'contact_phone',
            'external_link',
        ]

