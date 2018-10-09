import pickle

from django import forms
from django.forms import ModelForm

from entity.models.company import Company


class AddressWidget(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            forms.TextInput(),
            forms.TextInput()
        ]
        super(AddressWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return pickle.loads(value)
        else:
            return ['', '']


class AddressField(forms.fields.MultiValueField):
    widget = AddressWidget

    def __init__(self, *args, **kwargs):
        list_fields = [
            forms.fields.CharField(max_length=40),
            forms.fields.CharField(max_length=40)
        ]
        super(AddressField, self).__init__(list_fields, *args, **kwargs)

    def compress(self, values):
        return pickle.dumps(values)


class CompanyApplicationForm(ModelForm):
    address = AddressField()
    address.label = "Address"

    class Meta:
        model = Company

        fields = [
            'name',
            'contact_phone',
            'contact_email',
            'website',
            'summer_students',
            'industry',
            'type_of_business',
            'size',
            'specialist_area'
        ]


class EditCompanyForm(ModelForm):
    """
    Form for updating company information
    """

    class Meta:
        model = Company
        fields = (
            'name',
            'size',
            'industry',
            'specialist_area',
            'contact_phone',
            'contact_email',
            'website',
            'type_of_business',
            'address',
            'summer_students'
        )