from django.forms import Form
from django import forms


class LoginForm(Form):
    username = forms.CharField(label='Login')
    password = forms.CharField(widget=forms.PasswordInput())

