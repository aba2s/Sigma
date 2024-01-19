from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "Email...", "class": "form-control"}
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter password", "class": "form-control"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirm password", "class": "form-control"}
        )
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]
        widgets = {
            "username": forms.TextInput(
                attrs={"placeholder": "Username...", "class": "form-control"}
            ),
            "first_name": forms.TextInput(
                attrs={"placeholder": "First Name...", "class": "form-control"}
            ),
            "last_name": forms.TextInput(
                attrs={"placeholder": "Last Name...", "class": "form-control"}
            ),
        }
