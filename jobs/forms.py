import pickle

from django import forms
from django.forms import ModelForm

from jobs.models import Job


class JobCreationForm(ModelForm):

    class Meta:
        model = Job

        fields = [
            'title',
            'description',
            'location',
            'contact_email',
            'contact_phone',
            'expiry',
            'external_link',
        ]

