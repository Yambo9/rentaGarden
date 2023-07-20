from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model,logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
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
            if(contraseña == contraseña2):
                if(contraseña<8):
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
                    return redirect('home')  # Redirigir a la página de inicio después del registro exitoso
                else:
                   problem = "Las Contraseña ingresada es demasiado corta. Asegurate de que tenga un mínimo de 8 caracteres."
                   form = RegisterForm()
                   return render(request, 'register.html', {'form': form,'problem':problem})
            else:
                   problem = "Las contraseñas ingresadas no coinciden."
                   form = RegisterForm()
                   return render(request, 'register.html', {'form': form,'problem':problem})
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
            return redirect('home')
        form = AuthenticationForm()       
        return render(request,'signin.html',{'problem':'Usuario no encontrado o contraseña equivocada','form':form})
    
@login_required
def Profile(request):
    if request.user.is_authenticated:
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
                return redirect('profile')
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
