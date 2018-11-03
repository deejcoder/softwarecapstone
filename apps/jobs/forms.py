import pickle

from django import forms
from django.forms import ModelForm

from apps.jobs.models import Job


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

        
class EditJobForm(ModelForm):
    class Meta:
        model = Job

        fields = [
            'company',
            'title',
            'short_description',
            'description',
            'location',
            'contact_email',
            'contact_phone',
            'external_link',
            'expiry',
        ]

        widgets = {
            'description': forms.Textarea,
            'expiry': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }   
