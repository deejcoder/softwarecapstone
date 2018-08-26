"""
This view file consists of general pages e.g homepage, contact-us.
"""
from django.shortcuts import render
from django.views.generic.base import TemplateView


class Index(TemplateView):
	"""
	Render homepage
	"""

	template_name = 'index.html'
	def index(self, TemplateView):
		return render(request, 'index.html')


class ConsultApp(forms.Form):
	fname = forms.CharField(label='First name:', required=True, help_text='Hello!')
	lname = forms.CharField(label='Last name:', required=True)
	email = forms.EmailField(label='E-mail address:', required=True)
	address = forms.CharField(label='Address:', required=True, help_text='Good-bye!')
	city = forms.CharField(required=True)
	pcode = forms.IntegerField(label='Post Code:', required=True)


def application_form(request):
    if request.method == 'POST':
        form = ConsultApp();
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username_field')
            raw_password = form.cleaned_data.get('password_field')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = ConsultApp()
    return render(request, './templates/app_form.html', {'form': form})
