from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Region(models.Model):
    nombre = models.CharField(max_length=150)


class Ciudad(models.Model):
    nombre = models.CharField(max_length=150)
    region = models.ForeignKey(Region,on_delete=models.CASCADE)


class Comuna(models.Model):
    nombre = models.CharField(max_length=150)
    ciudad = models.ForeignKey(Ciudad,on_delete=models.CASCADE)


class Admin(models.Model):
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    rol = models.CharField(max_length=150)
    fecha_registro = models.DateTimeField(auto_now=True)


class Arrendatario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=15, unique=True)
    fecha_registro = models.DateTimeField(auto_now=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    numero_direccion = models.IntegerField(null=True, blank=True)
    numero_telefono = models.IntegerField(null=True, blank=True)
    ultimo_login = models.DateTimeField(auto_now=True, null=True, blank=True)

    
class Ejecutivo(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    rut = models.CharField(max_length=15)
    rol = models.CharField(max_length=100)
    FechaRegistro = models.DateTimeField(auto_now=True)
    ultimo_login = models.DateTimeField(auto_now=True,null=True,blank=True)


class Caracteristica(models.Model):
    titulo = models.CharField(max_length=150,null=True,blank=True)
    descripcion = models.TextField(max_length=500)


class Planta(models.Model):
    CATEGORIAS = (
        ('Arbol', 'Arbol'),
        ('Arbusto', 'Arbusto'),
        ('Flores', 'Flores'),
        ('Suculenta', 'Suculenta'),
        ('Cactus', 'Cactus'),
    )
    caracteristica = models.ForeignKey(Caracteristica,on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    nombre_cientifico = models.CharField(max_length=150)
    altura = models.DecimalField(max_digits=6, decimal_places=2)
    tamaño_m2 =  models.DecimalField(max_digits=5, decimal_places=2)
    peso =  models.DecimalField(max_digits=5, decimal_places=2)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    perenne = models.BooleanField(default=False)
    riego = models.CharField(max_length=200)
    cuidados = models.TextField()
    stock = models.IntegerField()
    valor = models.DecimalField(max_digits=8, decimal_places=2)

class Pedido(models.Model):
    arrendatario = models.ForeignKey(Arrendatario,on_delete=models.CASCADE)
    comuna = models.ForeignKey(Comuna,on_delete=models.CASCADE)
    direccion = models.CharField(max_length=200)
    numero = models.IntegerField()
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    hora_inicio = models.TimeField(null=True,blank=True)
    hora_termino = models.TimeField(null=True,blank=True)
    instrucciones = models.TextField(null=True,blank=True)
    peso =  models.DecimalField(max_digits=7, decimal_places=2,null=True,blank=True)
    valor =  models.DecimalField(max_digits=8, decimal_places=2,null=True,blank=True)
    valorFlete = models.DecimalField(max_digits=8, decimal_places=2,null=True,blank=True)

class Mensaje(models.Model):
    pedido = models.ForeignKey(Pedido,on_delete=models.CASCADE)
    ejecutivo = models.ForeignKey(Ejecutivo,on_delete=models.CASCADE)
    visto = models.BooleanField(default=False)
    asunto = models.CharField(max_length=200)
    mensaje = models.TextField()

class Planta_pedido(models.Model):
    pedido = models.ForeignKey(Pedido,on_delete=models.CASCADE)
    planta = models.ForeignKey(Planta,on_delete=models.CASCADE)
    cantidad = models.IntegerField()