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


class SeleccionarDireccionForm(forms.Form):
    comuna = forms.ModelChoiceField(queryset=Comuna.objects.all().order_by('nombre'), empty_label='Selecciona una comuna')
    calle = forms.CharField(max_length=150)
    numero = forms.CharField(max_length=10)
    depto = forms.CharField(max_length=10, required=False)
    indicaciones = forms.CharField(widget=forms.Textarea, required=False)


class CrearPlantaForm(forms.ModelForm):
    caracteristica = forms.ModelMultipleChoiceField(queryset=Caracteristica.objects.all())  # Ajusta el queryset
    
    class Meta:
        model = Planta
        fields = '__all__'

class PlantaForm(forms.ModelForm):
    class Meta:
        model = Planta
        fields = '__all__'


class MensajeAnonimoForm(forms.Form):
    nombre = forms.CharField(label="nombre", max_length=150, required=True)
    asunto = forms.CharField(label="asunto", max_length=200, required=False)
    email = forms.CharField(label="email", max_length=200, required=True)
    mensaje = forms.CharField(widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['class'] = 'form-control mb-4 rounded-5'
        self.fields['asunto'].widget.attrs['class'] = 'form-control mb-4 rounded-5'
        self.fields['email'].widget.attrs['class'] = 'form-control mb-4 rounded-5'
        self.fields['mensaje'].widget.attrs['class'] = 'form-control mb-4 rounded-5 col-12'

class RespuestaMensajeAnonimoForm(forms.Form):
    respuesta = forms.CharField(label="respuesta", required=True, widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['respuesta'].widget.attrs['class'] = 'form-control mb-4 rounded-5'

class BusquedaMensaje(forms.Form):
    busqueda = forms.CharField(label="respuesta", required=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['busqueda'].widget.attrs['class'] = 'form-control mb-4 rounded-5'




