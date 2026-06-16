from django import forms

# models
from django.contrib.auth.models import User
from accounts.models import (
    Masyarakat
)

class MasyarakatForm(forms.ModelForm):
    class Meta:
        model = Masyarakat
        fields = ["nik", "nama", "no_hp", "alamat"]
        exclude = ["user"]

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]