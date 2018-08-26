"""
Forms belonging to users or consultants.
"""
from django.forms import ModelForm
from .models import Consultant


class ConsultantApplicationForm(ModelForm):
    """
    A form to allow users to apply to become
    a consultant.
    """
    class Meta:
        model = Consultant
        fields = (
            'area_of_expertise',
            'services_offered',
            'work_phone',
            'website'
        )
