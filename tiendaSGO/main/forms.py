from django import forms
from django.utils.translation import gettext_lazy as _

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label=_("Usuario"))
    password = forms.CharField(max_length=100, label=_("Contraseña"), widget=forms.PasswordInput)

