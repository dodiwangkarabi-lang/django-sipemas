from django import forms

# forms
from django.contrib.auth.forms import UserCreationForm

# models
from accounts.models import (
    Masyarakat
)

class MasyarakatForm(forms.ModelForm):
    class Meta:
        model = Masyarakat
        fields = "__all__"
        

# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Masyarakat


class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )


class MasyarakatForm(forms.ModelForm):
    class Meta:
        model = Masyarakat
        exclude = ["user"]