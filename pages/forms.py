from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from account.models import Account
from django import forms

class CreateUserForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['username', 'email', 'password1', 'password2', 'meterID']
