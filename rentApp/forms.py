from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Arrendatario

class RegisterForm(forms.Form):
    nombres = forms.CharField(label="Nombres", max_length=150, required=True)
    apellidos = forms.CharField(label="Apellidos", max_length=150, required=True)
    email = forms.EmailField(label="Email", max_length=150, required=True)
    contraseña1 = forms.CharField(label="Contraseña", max_length=150, required=True)
    contraseña2 = forms.CharField(label="Repite la Contraseña", max_length=150, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombres'].widget.attrs['class'] = 'form-control mb-4 rounded-5'
        self.fields['apellidos'].widget.attrs['class'] = 'form-control mb-4 rounded-5'
        self.fields['email'].widget.attrs['class'] = 'form-control mb-4 rounded-5'
        self.fields['contraseña1'].widget.attrs['class'] = 'form-control mb-4 rounded-5'
        self.fields['contraseña2'].widget.attrs['class'] = 'form-control mb-4 rounded-5'


