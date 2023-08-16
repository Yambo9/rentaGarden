from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import *

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


class ArrendatarioForm(forms.ModelForm):
    class Meta:
        model = Arrendatario
        exclude = ['usuario', 'ultimo_login']

class EjecutivoForm(forms.Form):
    email = forms.EmailField(label="Correo Electrónico", max_length=150, required=True)
    nombre = forms.CharField(label="Nombres", max_length=200, required=True)
    apellido = forms.CharField(label="Apellidos", max_length=200, required=True)
    rut = forms.CharField(label="Rut", max_length=14, required=True)
    rol = forms.CharField(max_length=50)
    telefono = forms.IntegerField(required=True)

    contraseña = forms.CharField(label="Contraseña", max_length=150, required=True, widget=forms.PasswordInput)
    contraseña2 = forms.CharField(label="Repite la Contraseña", max_length=150, required=True, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['class'] = 'form-control mb-4 rounded-5'
        self.fields['apellido'].widget.attrs['class'] = 'form-control mb-4 rounded-5'
        self.fields['rut'].widget.attrs['class'] = 'form-control mb-4 rounded-5'
        self.fields['rol'].widget.attrs['class'] = 'form-control mb-4 rounded-5'
        self.fields['email'].widget.attrs['class'] = 'form-control mb-4 rounded-5'
        self.fields['telefono'].widget.attrs['class'] = 'form-control mb-4 rounded-5'
        self.fields['contraseña'].widget.attrs['class'] = 'form-control mb-4 rounded-5'
        self.fields['contraseña2'].widget.attrs['class'] = 'form-control mb-4 rounded-5'


class SeleccionarPlantaForm(forms.Form):
    cantidad = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'min': 1,
                'class': 'form-control mb-3 rounded-5 mt-5',
                'placeholder': 'Ingrese la cantidad de plantas a arrendar'}
        )
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CrearPlantaForm(forms.ModelForm):
    caracteristica = forms.ModelMultipleChoiceField(queryset=Caracteristica.objects.all())  # Ajusta el queryset
    
    class Meta:
        model = Planta
        fields = '__all__'