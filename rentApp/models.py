from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Region(models.Model):
    nombre = models.CharField(max_length=150)
    def __str__(self): 
        return self.nombre

class Ciudad(models.Model):
    nombre = models.CharField(max_length=150)
    region = models.ForeignKey(Region,on_delete=models.CASCADE)
    def __str__(self): 
        return self.nombre

class Comuna(models.Model):
    nombre = models.CharField(max_length=150)
    ciudad = models.ForeignKey(Ciudad,on_delete=models.CASCADE)
    def __str__(self): 
        return self.nombre

class Admin(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    rol = models.CharField(max_length=150)
    fecha_registro = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return self.nombre + " " + self.apellido + "(" + self.rol + ")"

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
    def __str__(self) -> str:
        return self.rut + " - " + self.usuario.first_name + " " + self.usuario.last_name

@receiver(post_save, sender=User)
def update_ultimo_login(sender, instance, created, **kwargs):
    if created:
        # If the user is newly created, do not update the Arrendatario
        return

    try:
        arrendatario = Arrendatario.objects.get(usuario=instance)
        arrendatario.ultimo_login = instance.last_login
        arrendatario.save()
    except Arrendatario.DoesNotExist:
        # If the associated Arrendatario does not exist, do not update anything
        pass

post_save.connect(update_ultimo_login, sender=User)

class Ejecutivo(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    rut = models.CharField(max_length=15)
    rol = models.CharField(max_length=100)
    telefono = models.IntegerField(null= True,blank=True)
    FechaRegistro = models.DateTimeField(auto_now=True)
    ultimo_login = models.DateTimeField(auto_now=True,null=True,blank=True)
    def __str__(self) -> str:
        return self.rut + " - " + self.nombre + " " + self.apellido

class Caracteristica(models.Model):
    titulo = models.CharField(max_length=150,null=True,blank=True)
    descripcion = models.TextField(max_length=500)
    def __str__(self) -> str:
        return self.titulo    

class Planta(models.Model):
    CATEGORIAS = (
        ('Arbol', 'Arbol'),
        ('Arbusto', 'Arbusto'),
        ('Flores', 'Flores'),
        ('Suculenta', 'Suculenta'),
        ('Cactus', 'Cactus'),
    )
    caracteristica = models.ManyToManyField(Caracteristica)
    nombre = models.CharField(max_length=150)
    nombre_cientifico = models.CharField(max_length=150)
    descripcion = models.TextField(default="",null=True,blank=True)
    altura = models.CharField(max_length=90)
    tamaño_m2 =  models.DecimalField(max_digits=5, decimal_places=2)
    peso =  models.DecimalField(max_digits=5, decimal_places=2)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    perenne = models.BooleanField(default=False)
    riego = models.CharField(max_length=500)
    cuidados = models.TextField()
    stock = models.IntegerField()
    floracion = models.CharField(max_length=100, null=True,blank=True)
    familia = models.CharField(max_length=150, null=True,blank=True)
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    imagen = models.ImageField(upload_to='plantas/', null=True, blank=True)
    def __str__(self) -> str:
        return self.nombre_cientifico + " (" + self.nombre + ")" 
    
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
    def __str__(self) -> str:
        return "Arriendo - " + self.arrendatario.usuario.first_name + " " + self.arrendatario.usuario.last_name + " - " + self.fecha_inicio 

class Mensaje(models.Model):
    pedido = models.ForeignKey(Pedido,on_delete=models.CASCADE)
    ejecutivo = models.ForeignKey(Ejecutivo,on_delete=models.CASCADE)
    visto = models.BooleanField(default=False)
    asunto = models.CharField(max_length=200)
    mensaje = models.TextField()
    def __str__(self) -> str:
        return self.pedido.arrendatario.usuario.first_name + self.pedido.arrendatario.usuario.last_name + " - " + self.ejecutivo.nombre + " " + self.ejecutivo.apellido
    
class Planta_pedido(models.Model):
    pedido = models.ForeignKey(Pedido,on_delete=models.CASCADE)
    planta = models.ForeignKey(Planta,on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    def __str__(self) -> str:
        return self.pedido.arrendatario.usuario.first_name + " " + self.pedido.arrendatario.usuario.last_name + " - " + self.planta.nombre