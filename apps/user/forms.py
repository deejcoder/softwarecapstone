"""
Forms belonging to users or consultants.
"""

from captcha.fields import ReCaptchaField
from django import forms
from django.forms import ModelForm

from .models import Consultant, User


class ConsultantApplicationForm(ModelForm):
    i_agree = forms.BooleanField()

    """
    A form to allow users to apply to become
    a consultant.
    """
    class Meta:
        model = Consultant
        fields = (
            'contact_phone',
            'contact_email',
            'website',
            'current_occupation',
            'area_of_expertise',
            'introduction',
            'services_offered',
        )


class EditConsultantForm(ModelForm):
    """
    Form to allow consultants to edit their details
    """

    class Meta:
        model = Consultant
        fields = (
            'contact_phone',
            'contact_email',
            'website',
            'current_occupation',
            'area_of_expertise',
            'introduction',
            'services_offered',
        )


class EditProfileForm(ModelForm):
    """
    Form for updating profile information
    """

    password = forms.CharField(required=False, widget=forms.PasswordInput)
    current_password = forms.CharField(required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'avatar',
            'first_name',
            'last_name',
            'email',
        )

        widgets = {
            'password': forms.PasswordInput,
        }

    def save(self, commit=True):
        """
        Sets the user's password
        """
        user = super(EditProfileForm, self).save(commit=False)
        password = self.cleaned_data['password']
        if password:
            user.set_password(password)

        if commit:
            user.save()
        return user


class UserRegistrationForm(ModelForm):
    """
    A form to allow users to apply to become
    a consultant.
    """

    confirm_password = forms.CharField(widget=forms.PasswordInput)
    captcha = ReCaptchaField()

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
