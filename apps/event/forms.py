from django import forms
from django.forms import ModelForm
from .models import Event


class CreateEventForm(ModelForm):

    class Meta:
        model = Event

        fields = {
            'entity',
            'title',
            'date',
            'time',
            'location',
            'description'
        }

        widgets = {
            'description': forms.Textarea,
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class EditEventForm(ModelForm):

    class Meta:
        model = Event

        fields = {
            'entity',
            'title',
            'date',
            'time',
            'location',
            'description'
        }

        widgets = {
            'description': forms.Textarea,
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }