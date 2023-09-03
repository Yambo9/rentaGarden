from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import *
from django.forms.widgets import SelectDateWidget, TimeInput, DateInput
from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm

#USUARIO
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

#USUARIO GENERAL
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


#ADMIN

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

class CrearPlantaForm(forms.ModelForm):
    caracteristica = forms.ModelMultipleChoiceField(queryset=Caracteristica.objects.all())  # Ajusta el queryset
    
    class Meta:
        model = Planta
        fields = '__all__'

class PlantaForm(forms.ModelForm):
    class Meta:
        model = Planta
        fields = '__all__'

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


#PEDIDO
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
    numero = forms.IntegerField()
    depto = forms.CharField(max_length=10, required=False)
    indicaciones = forms.CharField(widget=forms.Textarea, required=False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comuna'].widget.attrs['class'] = 'form-control mb-4 rounded-5'
        self.fields['calle'].widget.attrs['class'] = 'form-control mb-4 rounded-5'
        self.fields['numero'].widget.attrs['class'] = 'form-control mb-4 rounded-5'
        self.fields['depto'].widget.attrs['class'] = 'form-control mb-4 rounded-5 col-12'
        self.fields['indicaciones'].widget.attrs['class'] = 'form-control mb-4 rounded-5 col-12'

class SeleccionarFechaForm(forms.Form):
    diaInicio = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    horaInicio = forms.TimeField(widget=TimeInput(attrs={'type': 'time'}))
    fechaFin = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    horaFin = forms.TimeField(widget=TimeInput(attrs={'type': 'time'}))

    def clean(self):
        cleaned_data = super().clean()
        dia_inicio = cleaned_data.get('diaInicio')
        
        if dia_inicio and dia_inicio < datetime.now().date():
            self.add_error('diaInicio', "La fecha de inicio no puede ser anterior al día actual.")
        
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control mb-4 rounded-5'

class CrearUsuarioPedido(forms.Form):
    nombre = forms.CharField(max_length=80)
    rut = forms.CharField(max_length=15)
    email = forms.EmailField()
    telefono = forms.IntegerField()
    fecha_nacimiento = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['class'] = 'form-control mb-4 rounded-5'
        self.fields['rut'].widget.attrs['class'] = 'form-control mb-4 rounded-5'
        self.fields['email'].widget.attrs['class'] = 'form-control mb-4 rounded-5'
        self.fields['telefono'].widget.attrs['class'] = 'form-control mb-4 rounded-5 col-12'
        self.fields['fecha_nacimiento'].widget.attrs['class'] = 'form-control mb-4 rounded-5 col-12'


class Login2(forms.Form):
    login_email = forms.CharField(label="Email", max_length=150, required=True)
    contraseña = forms.CharField(label="Contraseña", max_length=150, required=True, widget=forms.PasswordInput )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login_email'].widget.attrs['class'] ='form-control mb-4 rounded-5'
        self.fields['contraseña'].widget.attrs['class'] ='form-control mb-4 rounded-5'
