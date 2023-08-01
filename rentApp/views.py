from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model,logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from django.contrib.auth.decorators import login_required
import random
from .models import *
from django.contrib import messages

# Create your views here.

def Home(request):
    print(request.user)
    return render(request,'index.html',{})



def Register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            nombres = form.cleaned_data['nombres']
            apellidos = form.cleaned_data['apellidos']
            email = form.cleaned_data['email']
            contraseña = form.cleaned_data['contraseña1']
            contraseña2 = form.cleaned_data['contraseña2']
            if contraseña == contraseña2:
                if len(contraseña) >= 8:
                    # Crear el usuario
                    User = get_user_model()
                    user = User.objects.create_user(username=email, email=email, password=contraseña)
                    user.first_name = nombres
                    user.last_name = apellidos
                    user.save()
                    print("Usuario guardado correctamente")
                    user = authenticate(request, username=email, password=contraseña)
                    if user is not None:
                        login(request, user)
                    return redirect('profile')  # Redirigir a la página de inicio después del registro exitoso
                else:
                    problem = "La contraseña ingresada es demasiado corta. Asegúrate de que tenga un mínimo de 8 caracteres."
            else:
                problem = "Las contraseñas ingresadas no coinciden."
        else:
            problem = "Hay errores en el formulario. Verifica los campos."

        # Si hay algún problema, renderizar la página con el formulario y el mensaje de error
        form = RegisterForm()
        return render(request, 'register.html', {'form': form, 'problem': problem})
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})


@login_required
def Logout(request):
    logout(request)
    return redirect('home')

def Signin(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request,'signin.html',{'form':form})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user) 
            return redirect('profile')
        form = AuthenticationForm()       
        return render(request,'signin.html',{'problem':'Usuario no encontrado o contraseña equivocada','form':form})
    
@login_required
def Profile(request):
    if request.user.is_authenticated:
        #REVISA SI ES ADMIN
        try:
            admin = Admin.objects.filter(usuario=request.user).first()
            if admin is None:
            #REVISA SI ES ARRENDATARIO
                try:
                    arrendatario = Arrendatario.objects.filter(usuario=request.user).first()
                    if arrendatario is None:
                        print('El usuario no tiene sus datos completos')
                        return render(request, 'profile.html', {})
                    else:
                        print('Arrendatario encontrado')
                        return render(request, 'profile.html', {'arrendatario': arrendatario})
                except Exception as e:
                    print('Ocurrió un error al cargar el Perfil:', e)
                    return redirect('home')
            else:
                print('ADMIN encontrado')
                return render(request, 'profile.html', {'admin': admin})
        except:
            print("ERROR AL BUSCAR AL ADMIN")
            return redirect('home')
    else:
        print('El usuario no está autenticado')
        return redirect('home')  # or redirect to the login page


  # Make sure to import the Comuna model

@login_required
def Crear_arrendatario(request):
    if request.method == 'POST':
        try:
            # ... other code

            if 8 <= len(request.POST['rut']) and len(request.POST['rut']) <= 12:
                # Get the Comuna object based on the ID from the form
                comuna_id = int(request.POST['comuna'])
                comuna_instance = Comuna.objects.get(pk=comuna_id)

                data = Arrendatario.objects.create(
                    usuario=request.user,
                    rut=request.POST['rut'],
                    fecha_nacimiento=request.POST['fecha_nacimiento'],
                    comuna=comuna_instance,  # Assign the Comuna instance, not the ID
                    direccion=request.POST['direccion'],
                    numero_direccion=request.POST['numero_direccion'],
                    numero_telefono=request.POST['numero_telefono'],
                )
                data.save()
                return redirect('menuArriendo')
            else:
                problem_message = 'El rut ingresado no cumple con la longitud esperada (entre 8 y 12 caracteres).'
                form = ArrendatarioForm(request.POST)
                return render(request, 'crear_arrendatario.html', {'form': form, 'problem': problem_message})

        except Exception as e:
            error_message = str(e)  # Get the error message from the exception
            form = ArrendatarioForm(request.POST)
            return render(request, 'crear_arrendatario.html', {'form': form, 'problem': 'Ocurrió un problema :('})
    
    else:
        form = ArrendatarioForm()  # Define the form for GET request
    return render(request, 'crear_arrendatario.html', {'form': form})

def Catalogo(request):
    try:
        arboles = Planta.objects.filter(categoria='Arbol')
        arbustos = Planta.objects.filter(categoria ='Arbusto')
        return render(request,'catalogo.html',{'arboles':arboles,'arbustos':arbustos})

    except:
        print("Ocurrio un error al cargar las plantas.")
        return redirect('home')
    
def DetallePlanta(request,id):
    try:
        plantita = Planta.objects.get(pk=id)
        return render(request,'detalle_planta.html',{'planta':plantita})
    except:
        print('Ocurrio un error al encontrar la planta')
        return redirect('home')
    

def menuArriendo(request):
    try:
        print('VIENDO SI EL USUARIO ESTA REGISTRADO')
        if(request.user.is_authenticated):
            print("EL USUARIO ESTA REGISTRADO")
            print("VIENDO SI LOS DATOS PERSONALES ESTAN COMPLETOS")
            try:
                arrendatario = Arrendatario.objects.filter(usuario = request.user).first()
                if(arrendatario is None):
                    print("LOS DATOS PERSONALES DEL USUARIO ESTAN INCOMPLETOS")
                    return render(request,'menuPedidos.html')
                else:
                    print("LOS DATOS PERSONALES DEL USUARIO ESTAN COMPLETOS")
                    return render(request,'menuPedidos.html',{'arrendatario':arrendatario})
            except:
                print("Ocurrio un problema al ver si el usuario tiene datos personales Completados")
                return redirect('profile')
        else:
            print("El usuario no esta registrado. Mandando al ususario al formulario de registro.")
            return render(request,'menuPedidos.html')
    except:
        print('Ocurrio un error al encontrar al Usuario')
        return render('home')

def seleccionar_plantas(request):
    plantas = Planta.objects.all()
    if request.method == 'POST':
        form = SeleccionarPlantaForm(request.POST)
        if form.is_valid():
            planta = form.cleaned_data['planta']
            cantidad = form.cleaned_data['cantidad']
            
            # Verificar si la cantidad seleccionada supera el stock disponible
            if cantidad > planta.stock:
                error_message = "No hay suficiente stock disponible para esa cantidad."
                return render(request, 'seleccionar_plantas.html', {'form': form, 'plantas': plantas, 'error_message': error_message})
            
            # Crear el registro de Planta_pedido
            planta_pedido = Planta_pedido(pedido=None, planta=planta, cantidad=cantidad)
            planta_pedido.save()

    else:
        form = SeleccionarPlantaForm()

    return render(request, 'seleccionar_plantas.html', {'form': form, 'plantas': plantas})


def MenuEjecutivos(request):
    try:
        admin = Admin.objects.get(usuario=request.user)
        if admin is not None:
            print('Eres admin')
            try:
                ejecutivos = Ejecutivo.objects.all()
                print('Se encontraron los Ejecutivos')
                return render(request, 'menu_ejecutivos.html', {'ejecutivos': ejecutivos})

            except:    
                print("Ocurrio un error al encontrar al ejecutivo.")
                return redirect('home')
        else:
            print("No eres Admin")
            return redirect('home')
    except:
        print('Ocurrio un error al ver si eres Admin')
        return redirect('home')

def CrearEjecutivo(request):
    if request.method == 'POST':
        form = EjecutivoForm(request.POST)
        if form.is_valid():
            # Código para guardar al ejecutivo
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            email = form.cleaned_data['email']
            contraseña = form.cleaned_data['contraseña']
            contraseña2 = form.cleaned_data['contraseña2']
            if(contraseña == contraseña2):
                if(len(contraseña) >= 8):
                    # Crear el usuario
                    User = get_user_model()
                    user = User.objects.create_user(username=email, email=email, password=contraseña)
                    user.first_name = nombre
                    user.last_name = apellido
                    user.save()
                    print("Usuario guardado correctamente")
                    # Ahora guardando ejecutivo
                    rut = form.cleaned_data['rut']
                    rol = form.cleaned_data['rol']
                    telefono = form.cleaned_data['telefono']
                    ejecutivo = Ejecutivo.objects.create(
                        usuario=user,
                        nombre=nombre,
                        apellido=apellido,
                        rut=rut,
                        rol=rol,
                        telefono=telefono
                    )
                    ejecutivo.save()
                    print('El usuario fue guardado correctamente')
                    return redirect('menu_ejecutivos')
        else:
            # Si el formulario no es válido, renderizar el formulario con los errores
            return render(request, 'crear_ejecutivo.html', {'form': form})
    else:
        form = EjecutivoForm()
        return render(request, 'crear_ejecutivo.html', {'form': form})

def ModificarEjecutivo(request, id):
    try:
        ejecutivo = Ejecutivo.objects.get(usuario=id)
        user = ejecutivo.usuario

        if request.method == 'POST':
            form = EjecutivoForm(request.POST)

            if form.is_valid():
                user.email = form.cleaned_data['email']
                user.set_password(form.cleaned_data['contraseña'])
                user.save()

                ejecutivo.nombre = form.cleaned_data['nombre']
                ejecutivo.apellido = form.cleaned_data['apellido']
                ejecutivo.rut = form.cleaned_data['rut']
                ejecutivo.rol = form.cleaned_data['rol']
                ejecutivo.telefono = form.cleaned_data['telefono']
                ejecutivo.save()

                return redirect('menu_ejecutivos')
        else:
            form = EjecutivoForm(initial={
                'email': user.email,
                'nombre': ejecutivo.nombre,
                'apellido': ejecutivo.apellido,
                'rut': ejecutivo.rut,
                'rol': ejecutivo.rol,
                'telefono': ejecutivo.telefono
            })

        return render(request, 'modificar_ejecutivos.html', {'form': form, 'instancia': ejecutivo})
    except:
        print('Ocurrió un error al modificar al usuario.')
        return redirect('home')

def EliminarEjecutivo(request,id):
    try:
        if request.method == 'GET':
            usuario = Ejecutivo.objects.get(usuario = id)
            return render(request,'eliminar_ejecutivo.html',{'ejecutivo':usuario})
        else:
            usuario = User.objects.get(id = id)
            usuario.delete()
            return redirect('menu_ejecutivos')
    except:
        print("Ocurrio un error al eliminar al ejecutivo.")
        return redirect('home')