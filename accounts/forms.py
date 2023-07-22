from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


strong_password = RegexValidator(
    regex="^[a-zA-Z0-9_]*$",
    message='Only alphanumeric characters are allowed.',
    code='Invalid password format')

class RegisterForm(UserCreationForm):
	email = forms.EmailField()
	# password1 = forms.CharField(min_length=8,
	# 	widget=forms.PasswordInput, validators=[strong_password])
	# password2 = forms.CharField(min_length=8,
	# 	widget=forms.PasswordInput, validators=[strong_password])
	
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'password1',
			'password2'
		]