from django import forms
from captcha.fields import ReCaptchaField


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=30)
    subject = forms.CharField(max_length=50)
    message = forms.CharField(widget=forms.Textarea, max_length=1000)
    captcha = ReCaptchaField()

