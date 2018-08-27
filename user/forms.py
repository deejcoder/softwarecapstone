"""
Forms belonging to users or consultants.
"""
from django.forms import ModelForm
from django import forms
from .models import Consultant, User


class ConsultantApplicationForm(ModelForm):
    """
    A form to allow users to apply to become
    a consultant.
    """
    class Meta:
        model = Consultant
        fields = (
            'services_offered',
            'current_occupation',
            'work_phone',
            'website'
        )


class UserRegistrationForm(ModelForm):
    """
    A form to allow users to apply to become
    a consultant.
    """

    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        )

        widgets = {
            'password': forms.PasswordInput,
        }

    def clean(self):
        """
        Check if passwords match
        """
        cleaned_data = super(UserRegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', "The password doesn't match")
        
        return cleaned_data

    def save(self, commit=True):
        """
        Sets the user's password
        """
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()
        return user
