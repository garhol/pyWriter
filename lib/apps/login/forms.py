from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email")
