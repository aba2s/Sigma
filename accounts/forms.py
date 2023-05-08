from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
	email = forms.EmailField()
	# secret_code = forms.CharField(
	#	widget=forms.PasswordInput,
	#    max_length=4)

	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'password1',
			'password2'
		]