
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder":"usuario",
                "class":"form-control",
            }
        )
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"Senha",
                "class":"form-control",
            }
        )
    )
    class Meta:
        fields = ('username','password')