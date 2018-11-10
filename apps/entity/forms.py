import pickle

from django import forms
from django.forms import ModelForm

from apps.entity.models import Member
from apps.entity.models.company import Company
from apps.entity.models.group import Group
from apps.entity.models import Entity


class CompanyApplicationForm(ModelForm):

    class Meta:
        model = Company

        fields = [
            'name',
            'address',
            'contact_phone',
            'contact_email',
            'website',
            'summer_students',
            'industry',
            'type_of_business',
            'size',
            'introduction',
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
            'address',
            'size',
            'industry',
            'introduction',
            'specialist_area',
            'contact_phone',
            'contact_email',
            'website',
            'type_of_business',
            'address',
            'summer_students'
        )


class EditAvatarForm(ModelForm):
    """
    Form to allow groups and companies to update their
    profile avatar
    """

    class Meta:
        model = Entity
        fields = (
            'avatar',
        )


class GroupApplicationForm(ModelForm):
    i_agree = forms.BooleanField()

    class Meta:
        model = Group
        fields = {
            'name',
            'website',
            'introduction',
            'description',
        }


class EditGroupForm(ModelForm):
    """
    Form for updating group information
    """

    class Meta:
        model = Group
        fields = (
            'name',
            'website',
            'introduction',
            'description'
        )


class AddMembeerForm(forms.Form):
    """
    Allows some entity to add members to their entity
    """

    username = forms.CharField(label='Username', max_length=50)
    role = forms.ChoiceField(label='User\'s role', choices=Member.Roles.choices)
    

