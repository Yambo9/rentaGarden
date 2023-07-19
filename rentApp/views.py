from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model,logout
from django.contrib.auth.forms import AuthenticationForm

from .forms import RegisterForm
from .models import *

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

def Logout(request):
    logout(request)
    return redirect('home')

def Login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request,'signup.html',{'form':form})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)        
        return render(request,'signup.html',{'problem':'Usuario no encontrado'})
    