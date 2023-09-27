from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model,logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import F, Sum
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rentaPlant import settings
from django.contrib import messages 
from django.core.cache import cache
from django.contrib.auth.models import User

# Create your views here.
#VISTAS GENERALES DE USO PUBLICO
def Home(request):
    print(request.user)
    return render(request,'index.html',{})

def Mensaje_Anonimo(request):
    form = MensajeAnonimoForm()
    try:
        if request.method == 'GET':
            return render(request,'mensaje_anonimo.html',{'form':form})
        else:
            print(request.POST)
            if len(request.POST['nombre']) < 5:
                print("Nombre ingresado es muy corto")
                return render(request,'mensaje_anonimo.html',{'form':form,'problem':"El nombre ingresado es demasiado corto, ingreselo nuevamente pero más completo."})
            else:
                if '.' not in request.POST['email']:
                    print('EL email ingresado no tiene un punto. Intentelo nuevamente con un correo valido.')
                    return render(request,'mensaje_anonimo.html',{'form':form,'problem':"EL email ingresado no tiene un punto. Intentelo nuevamente con un correo valido."})
                else:
                    if '@' not in request.POST['email']:
                        print('EL email ingresado no tiene un @. Intentelo nuevamente con un correo valido.')
                        return render(request,'mensaje_anonimo.html',{'form':form,'problem':"EL email ingresado no tiene un @. Intentelo nuevamente con un correo valido."})
                    else:
                        if len(request.POST['mensaje'])<15:
                            print('EL mensaje es demasiado corto, debe tener a lo menos 16 caracteres.')
                            return render(request,'mensaje_anonimo.html',{'form':form,'problem':"EL mensaje es demasiado corto, debe tener a lo menos 16 caracteres."})
                        else:
                            mensaje = MensajeAnonimo.objects.create(
                                nombre=request.POST['nombre'],
                                asunto = request.POST['asunto'],
                                email = request.POST['email'],
                                mensaje = request.POST['mensaje'])
                            mensaje.save()

                            #ENVIANDO EL CORREO
                            nombre = request.POST['nombre']
                            asunto = request.POST['asunto']
                            email = request.POST['email']
                            message = request.POST['mensaje']
                            template = render_to_string('email_template.html',{
                                'nombre':nombre,
                                'asunto':asunto,
                                'email':email,
                                'message':message
                            })
                            email = EmailMessage(
                                asunto,
                                template,
                                settings.EMAIL_HOST_USER,
                                ['rentagardencontrol@gmail.com','tomasvalverdepresidente@gmail.com']
                            )
                            email.fail_silently = False
                            email.send()
                            messages.success(request,'Se ha enviado un correo.')
                            #El mail se manda
                            return render(request,'mensaje_anonimo.html',{'messages':'Tu Mensaje fue enviado correctamente! Te responderemos a la brevedad','form':form})
    except:
        print("Ocurrio un error al enviar el mensaje")
        return render(request,'mensaje_anonimo.html',{'form':form})

def Catalogo(request):
    try:
        arboles = Planta.objects.filter(categoria='Arbol', archivada=False)
        arbustos = Planta.objects.filter(categoria ='Arbusto', archivada=False)
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
    
def About(request):
    return render(request,'about.html',{})

def Info(request):
    return render(request,'info_arriendo.html')


#LOGICA USUARIO
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
def Crear_arrendatario(request):
    if request.method == 'POST':
        try:
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



#LOGICA PEDIDO
def seleccionar_plantas_pedido(request):
    try:
        #RECOPILANDO LOS DATOS
        arbol = Planta.objects.filter(categoria='Arbol', archivada=False)
        arbusto = Planta.objects.filter(categoria='Arbusto', archivada=False)
        datosPedido = request.session.get('misPlantitas', [])
        plantas_seleccionadas = []

        for pedido in datosPedido:
            planta_id = pedido['id']
            cantidad = pedido['cantidad']
            planta = Planta.objects.get(pk=planta_id)
            plantas_seleccionadas.append({'planta': planta, 'cantidad': cantidad, 'subtotal': planta.valor * cantidad,'peso':planta.peso*cantidad})
                
        total_plantas = sum(item['cantidad'] for item in datosPedido)
        valor_total = sum(item['subtotal'] for item in plantas_seleccionadas)  # Calcular el valor total
        peso_total = sum(item['peso'] for item in plantas_seleccionadas)
                    
        if request.method == 'GET':
            return render(request, 'pedido_seleccionar_plantas.html', {'arbol': arbol, 'arbusto': arbusto,
                                                                'datos': plantas_seleccionadas,
                                                                'conteo': total_plantas,
                                                                'valor_formateado': valor_total,
                                                                'peso_total':peso_total})
        else:
            #SE HACE UN POST
            print("Si hay plantas")
            if len(plantas_seleccionadas)>0:
                print("Hay plantas seleccionadas enviando al proximo paso")
                return redirect('direccion_pedido')
            else:
                return render(request, 'pedido_seleccionar_plantas.html', {'arbol': arbol, 'arbusto': arbusto,
                                                                    'datos': plantas_seleccionadas,
                                                                    'conteo': total_plantas,
                                                                    'valor_formateado': valor_total,
                                                                    'peso_total':peso_total,
                                                                    'problem':'*Se deben seleccionar plantas poder hacer un envío'})                

    except KeyError as e:
        print('Ocurrió un problema al encontrar las plantas del pedido:', e)
        return render(request, 'pedido_seleccionar_plantas.html', {'arbol': arbol, 'arbusto': arbusto,
                                                            'conteo': 0})
  
def detalle_seleccion_plantas(request, id):
    planta = Planta.objects.filter(pk=id).first()
    form = SeleccionarPlantaForm()
    
    if request.method == 'POST':
        if 'misPlantitas' not in request.session:
            request.session['misPlantitas'] = []
        
        #REVISANDO SI YA ESTA LA ID EN LA LISTA
        datosPlantas = request.session.get('misPlantitas',[])
        estaEnLista = False
        for a in datosPlantas:
            if a['id'] == id:
                print("La id de la planta ya esta en la lista.")
                estaEnLista = True

        if estaEnLista:
            return render(request, 'detalle_seleccion_plantas.html', {'planta': planta, 'form': form, 'problem':'La planta que ingresaste ya esta en su lista. Si quiere agregar más Modifique la que ya tiene en su lista de pedido.'})

        else:
            #AGREGANDO LA PLANTA A LA LISTA
            data = {'id': planta.pk, 'cantidad': int(request.POST.get('cantidad', 0))}
            request.session['misPlantitas'].append(data)
            request.session.modified = True  # Marcar la sesión como modificada
            #DIRECCIONANDO AL MENU
            print(request.session.get('misPlantitas', 'No hay nada'))
            return redirect('seleccionar_plantas')

    else:
        return render(request, 'detalle_seleccion_plantas.html', {'planta': planta, 'form': form})
    
def Direccion_pedido(request):
    if request.session.get("miDireccion") is not None:
        return redirect('fecha_pedido')
    else:
        form = SeleccionarDireccionForm()
        if request.method == 'POST':
            try:
                # Manejar el envío del formulario aquí
                comuna = request.POST['comuna']
                calle= request.POST['calle']
                numero= request.POST['numero']
                depto= request.POST['depto']
                indicaciones= request.POST['indicaciones']
                request.session["miDireccion"] = {'comuna':comuna,'calle':calle,'numero':numero,'depto':depto,'indicaciones':indicaciones,'volver':False}
                datos = request.session.get('miDireccion')
                print(datos)
                print("Datos guardados temporalmente")
                return redirect('fecha_pedido')
            except:
                print("Ocurrio un error al guardar la direccion")
                return render(request,'pedido_direccion.html',{'form':form})
        else:
            return render(request, 'pedido_direccion.html', {'form': form})

def Eliminar_seleccion(request, id):
    try:
        datosPedido = request.session.get('misPlantitas', [])
        
        for index, item in enumerate(datosPedido):
            if item['id'] == id:
                del datosPedido[index]
                break
        
        request.session['misPlantitas'] = datosPedido
    except:
        pass
    
    return redirect('seleccionar_plantas')

def Fecha_pedido(request):
    form = SeleccionarFechaForm()
    if request.session.get("miFecha") is not None:
        print("Hay una fecha registrada")
        return redirect('pagame')
    else:    
        if request.method == "POST":
            print("Se esta ejecutando el form")
            form = SeleccionarFechaForm(request.POST)
            if form.is_valid():
                diaInicio = form.cleaned_data['diaInicio']
                horaInicio = form.cleaned_data['horaInicio']
                diaFin = form.cleaned_data['fechaFin']
                horaFin = form.cleaned_data['horaFin']
                
                if diaInicio < datetime.now().date():
                    form.add_error('diaInicio', "La fecha de inicio no puede ser anterior al día actual.")
                    print("La fecha es antigua")
                else:
                    if diaInicio > diaFin:
                        form.add_error('diaInicio', "La fecha de inicio no puede ser anterior a la fecha de fin del arriendo.")
                        print("La fecha es antigua")
                    else:
                        diferencia_dias = (diaFin - diaInicio).days
                        request.session['miFecha'] = {
                            'diaInicio': diaInicio.strftime('%Y-%m-%d'),
                            'horaInicio': horaInicio.strftime('%H:%M:%S'),  # Convertir a cadena de tiempo
                            'diaFin': diaFin.strftime('%Y-%m-%d'),
                            'horaFin': horaFin.strftime('%H:%M:%S'),  # Convertir a cadena de tiempo
                            'diferencia_dias': diferencia_dias,
                            'volver':False
                        }
                        print(request.session.get('miFecha'))
                        print(request.session.get('miDireccion'))
                        print(request.session.get('misPlantitas'))
                        return redirect('pagame')
            else:
                print("El formulario no es valido")
        return render(request, 'pedido_fecha.html', {'form': form})

def Pagame(request):
    try:
        flete = calcularFlete(request)
        listado_plantas=listadoPlantas(request)
        valor_plantas = costoPlantas(request)
        direccion = recibirDireccion(request)
        fecha = recibirFecha(request)
        precioTotal = flete['precio_flete'] + valor_plantas
        print(precioTotal)
        return render(request,'pedido_valores_pagos.html',{'fecha':fecha,'flete':flete,'listado_plantas':listado_plantas,'valor_plantas':valor_plantas,'direccion':direccion,'total':precioTotal})
    except:
        print("Ocurrio un problema")
        return render(request,'pedido_valores_pagos.html',{})

def Datos_personales_pedido(request):
    if request.user.is_authenticated:
        return redirect('pagame')

    loginForm = Login2()
    crearForm = CrearUsuarioPedido()

    if request.method == 'POST':
        if 'login_form_submit' in request.POST:
            loginForm = Login2(request.POST)
            if loginForm.is_valid():
                # Procesar el formulario de inicio de sesión
                print("Se activó el formulario de inicio de sesión")
                # Verificar si el usuario existe
                user = authenticate(request, username=request.POST['login_email'], password=request.POST['contraseña'])
                if user is not None:
                    print("El usuario fue reconocido")
                    login(request, user)
                    return redirect('pagame')  # Redirigir a la página de perfil o donde desees

                else:
                    print("El usuario no fue reconocido")
                    # Renderizar el formulario de inicio de sesión con un mensaje de error
                    loginProblem = 'El usuario o la contraseña son incorrectos'
                    return render(request, 'pedido_datos_personales.html', {'loginForm': loginForm, 'crearForm': crearForm, 'loginProblem': loginProblem})

        elif 'crear_form_submit' in request.POST:
            crearForm = CrearUsuarioPedido(request.POST)
            if crearForm.is_valid():
                print("Se activó el formulario de ingreso de datos personales")
                # Procesar el formulario de creación de usuario
                nombre = crearForm.cleaned_data['nombre']
                rut = crearForm.cleaned_data['rut']
                telefono = crearForm.cleaned_data['telefono']
                email = crearForm.cleaned_data['email']
                fecha_nacimiento = crearForm.cleaned_data['fecha_nacimiento']
                # Revisando si la longitud del rut está bien
                if len(rut) < 11 and len(rut) > 8:
                    # La longitud del rut está bien, seguimos al próximo paso
                    print("La longitud del rut es la correcta")
                    # Revisando si el rut ya está en la base de datos
                    filtrado = Arrendatario.objects.filter(rut=rut).first()
                    if filtrado is None:
                        # No se encontró otro arrendatario con este rut, seguimos al próximo paso
                        print("El rut no está en la db")
                        # Revisando si el correo electrónico está en la DB
                        filtradoMail = User.objects.filter(email=email).first()
                        if filtradoMail is None:
                            # No se encontró el correo en la db, seguimos al próximo paso
                            print("No se encontró el correo en la db")
                            # Revisando la longitud del número telefónico
                            if len(str(telefono)) >= 7 and len(str(telefono)) <= 11:
                                # La longitud del número telefónico es la correcta, seguimos al próximo paso
                                print("Longitud del número telefónico es la correcta")
                                # PROCEDIENDO A CREAR AL USUARIO Y ARRENDATARIO
                                # --------------------------------------------------------
                                # Crear el usuario
                                user = get_user_model()
                                nuevo_usuario = user.objects.create_user(username=email, email=email, password=rut)
                                nuevo_usuario.save()
                                print("Usuario guardado correctamente")
                                nuevo_usuario = authenticate(request, username=email, password=rut)
                                if nuevo_usuario is not None:
                                    login(request, nuevo_usuario)
                                    print("Se creó correctamente al usuario")
                                    # Creando el arrendatario
                                    arrendatario = Arrendatario.objects.create(usuario=nuevo_usuario, rut=rut,
                                                                               fecha_nacimiento=fecha_nacimiento,
                                                                               numero_telefono=telefono)
                                    arrendatario.save()
                                    if arrendatario is not None:
                                        print("Se guardó todo correctamente")
                                        return redirect('pagame')
                                    else:
                                        print("Ocurrió un problema al registrar al arrendatario")
                                        return render(request, 'pedido_datos_personales.html',
                                                      {'loginForm': loginForm, 'crearForm': crearForm})
                                else:
                                    print("Ocurrió un problema al registrar al usuario")
                                    return render(request, 'pedido_datos_personales.html',
                                                  {'loginForm': loginForm, 'crearForm': crearForm})

                                # --------------------------------------------------------
                            else:
                                # La longitud del número telefónico es errónea
                                print("Longitud del número telefónico es errónea")
                                crearProblem = 'El número de teléfono ingresado no tiene la longitud correcta.'
                                return render(request, 'pedido_datos_personales.html',
                                              {'loginForm': loginForm, 'crearForm': crearForm, 'crearProblem': crearProblem})

                        else:
                            # El correo ya está en la db
                            print("El correo se encontró en la db")
                            crearProblem = 'El correo electrónico ingresado ya se encuentra registrado.'
                            return render(request, 'pedido_datos_personales.html',
                                          {'loginForm': loginForm, 'crearForm': crearForm, 'crearProblem': crearProblem})
                    else:
                        # El rut está en la db
                        print("El rut está en la db")
                        crearProblem = 'El rut ingresado ya está registrado'
                        return render(request, 'pedido_datos_personales.html',
                                      {'loginForm': loginForm, 'crearForm': crearForm, 'crearProblem': crearProblem})
                else:
                    # Longitud del rut incorrecta
                    print("La longitud del rut es incorrecta")
                    crearProblem = 'El rut ingresado es demasiado corto'
                    return render(request, 'pedido_datos_personales.html',
                                  {'loginForm': loginForm, 'crearForm': crearForm, 'crearProblem': crearProblem})
        else:
            print("No se está ejecutando ninguna wea")

    return render(request, 'pedido_datos_personales.html', {'loginForm': loginForm, 'crearForm': crearForm})


#Fuciones para calculo final
def calcularFlete(request):
    #recibiendo la comuna donde sera el arriendo
    direccion = request.session.get('miDireccion') 
    comuna = direccion['comuna']
    comunita = Comuna.objects.filter(id=comuna).first()
    precio_base=10000
    #Recibiendo listado de plantas
    datosPedido = request.session.get('misPlantitas', [])
    plantas_seleccionadas = []
    for pedido in datosPedido:
        planta_id = pedido['id']
        cantidad = pedido['cantidad']
        planta = Planta.objects.get(pk=planta_id)
        plantas_seleccionadas.append({'planta': planta, 'cantidad': cantidad, 'subtotal': planta.valor * cantidad,'peso':planta.peso*cantidad})

    #Calculo Peso Total    
    peso_total = sum(item['peso'] for item in plantas_seleccionadas)

    if int(comuna) == 1:
        distancia = 100
    elif int(comuna) == 2:
        distancia = 5
    elif int(comuna) == 3:
        distancia = 30
    elif int(comuna) == 4:
        distancia = 30.3
    elif int(comuna) == 5:
        distancia = 60
    elif int(comuna) == 6:
        distancia = 47
    elif int(comuna) == 7:
        distancia = 50
    elif int(comuna) == 8:
        distancia = 80
    elif int(comuna) == 9:
        distancia = 60
    elif int(comuna) == 10:
        distancia = 55
    elif int(comuna) == 11:
        distancia = 65
    elif int(comuna) == 12:
        distancia = 40
    elif int(comuna) == 13:
        distancia = 165
    elif int(comuna) == 14:
        distancia = 55
    elif int(comuna) == 15:
        distancia = 65
    elif int(comuna) == 16:
        distancia = 88
    elif int(comuna) == 17:
        distancia = 135
    elif int(comuna) == 18:
        distancia = 25
    elif int(comuna) == 19:
        distancia = 24
    elif int(comuna) == 20:
        distancia = 18
    elif int(comuna) == 21:
        distancia = 34
    elif int(comuna) == 22:
        distancia = 18
    elif int(comuna) == 23:
        distancia = 6
    elif int(comuna) == 24:
        distancia = 10
    elif int(comuna) == 25:
        distancia = 28
    elif int(comuna) == 26:
        distancia = 33
    elif int(comuna) == 27:
        distancia = 35
    elif int(comuna) == 28:
        distancia = 46
    elif int(comuna) == 29:
        distancia = 10
    elif int(comuna) == 30:
        distancia = 10
    elif int(comuna) == 31:
        distancia = 18
    elif int(comuna) == 32:
        distancia = 30
    elif int(comuna) == 33:
        distancia = 22
    elif int(comuna) == 34:
        distancia = 20
    elif int(comuna) == 35:
        distancia = 40
    elif int(comuna) == 36:
        distancia = 23
    elif int(comuna) == 37:
        distancia = 25
    elif int(comuna) == 38:
        distancia = 37
    elif int(comuna) == 39:
        distancia = 15
    elif int(comuna) == 40:
        distancia = 30
    elif int(comuna) == 41:
        distancia = 23
    elif int(comuna) == 42:
        distancia = 22
    elif int(comuna) == 43:
        distancia = 5
    elif int(comuna) == 44:
        distancia = 20
    elif int(comuna) == 45:
        distancia = 21
    elif int(comuna) == 46:
        distancia = 27
    elif int(comuna) == 47:
        distancia = 31
    elif int(comuna) == 48:
        distancia = 15
    elif int(comuna) == 50:
        distancia = 63
    elif int(comuna) == 52:
        distancia = 70
    elif int(comuna) == 53:
        distancia = 49
    elif int(comuna) == 54:
        distancia = 53
    elif int(comuna) == 55:
        distancia = 58

    precio_flete = int(precio_base + int(peso_total) * (distancia * 2))

    return {'peso_total':peso_total,'precio_flete':precio_flete,'comuna':comunita}

def listadoPlantas(request):
    datosPedido = request.session.get('misPlantitas', [])
    plantas_seleccionadas = []
    for pedido in datosPedido:
        planta_id = pedido['id']
        cantidad = pedido['cantidad']
        planta = Planta.objects.get(pk=planta_id)
        plantas_seleccionadas.append({'planta': planta, 'cantidad': cantidad, 'subtotal': planta.valor * cantidad,'peso':planta.peso*cantidad})
    return plantas_seleccionadas 

def costoPlantas(request):
    #Recibiendo listado de plantas
    datosPedido = request.session.get('misPlantitas', [])
    plantas_seleccionadas = []
    for pedido in datosPedido:
        planta_id = pedido['id']
        cantidad = pedido['cantidad']
        planta = Planta.objects.get(pk=planta_id)
        plantas_seleccionadas.append({'planta': planta, 'cantidad': cantidad, 'subtotal': planta.valor * cantidad,'peso':planta.peso*cantidad})

    #Calculo Peso Total    
    valor_total = sum(item['subtotal'] for item in plantas_seleccionadas)
    return valor_total

def recibirDireccion(request):
    try:
        direccion = request.session.get('miDireccion')
        return direccion
    except:
        print("Ocurrio un error")
        return None

def recibirFecha(request):
    try:
        fecha = request.session.get('miFecha')
        return fecha
    except:
        print("Ocurrió un error. (Fecha)")
        return None

#Volver pedido
def Volver_direccion(request):
    del request.session['miDireccion']
    return redirect('direccion_pedido')

def Volver_fecha(request):
    del request.session['miFecha']
    return redirect('fecha_pedido')






#LOGICA ADMIN
@login_required
def Menu_mensajes(request):
    #revisando si es admin
    
        admin = Admin.objects.filter(usuario=request.user).first()
        if request.method == 'GET':
            if admin is not None:
                mensajes = MensajeAnonimo.objects.filter(leido=False)
                mensajesLeidos = MensajeAnonimo.objects.filter(leido=True).order_by('-fecha')[:10]
                form = BusquedaMensaje()
                return render(request, 'menu_mensajes.html',{'mensajes':mensajes,'mensajesLeidos':mensajesLeidos,'form':form})
            else:
                print("No tienes las credenciales para estar aca.")
                return redirect('home')
        else:
            print("Realizando busqueda....")

            informacionFiltrada = MensajeAnonimo.objects.filter(nombre__contains=request.POST['nombre'].order_by('-fecha'))
            return render(request,'busqueda_mensajes.html',{'busqueda':informacionFiltrada})
    
        print("Ocurrio un error al encontrar los mensajes")
        return redirect('home')

@login_required    
def Leer_mensaje(request,id):
        mensaje = MensajeAnonimo.objects.filter(pk=id).first()
        respuesta = RespuestaMensajeAnonimo.objects.filter(mensajeAnonimo = mensaje)
        form = RespuestaMensajeAnonimoForm()
        if request.method == 'GET':
            #Encontrando el mensaje
            if mensaje is not None:
                print("El mensaje existe")
                if mensaje.leido == False:
                    mensaje.leido = True
                    mensaje.save()
                if respuesta is not None:
                    return render(request, 'leer_mensaje.html',{'mensaje':mensaje,'respuesta':respuesta,'form':form})
                else:
                    return render(request, 'leer_mensaje.html',{'mensaje':mensaje,'form':form})

            else:
                print("MENSAJE NO EXISTE")
                return redirect('menu_mensajes')
        else:
            print("Generando respuesta")
            admins = Admin.objects.filter(usuario=request.user).first()
            respuestita = RespuestaMensajeAnonimo.objects.create(
                mensajeAnonimo=mensaje,
                admin=admins,
                respuesta=request.POST['respuesta'],
            )
            respuestita.save()
            print("El mensaje de respuesta fue guardado correctamente")
            #ENVIANDO EL EMAIL
            correo = mensaje.email
            mensajito   = respuestita.respuesta
            asunto = "Respuesta Rentagarden"
            template = render_to_string('RespuestaTemplate.html',{
                'mensajito':mensajito
            })
            email = EmailMessage(
                asunto,  # Asunto del correo
                template,  # Contenido del correo generado con render_to_string
                settings.EMAIL_HOST_USER,
                [correo]
            )
            email.fail_silently = False
            email.send()
            messages.success(request,'Se ha enviado un correo.')
            #El mail se manda
            return redirect('menu_mensajes')

            return redirect('menu_mensajes')
   
        print("Ocurrio un error al Leer el mensaje")
        return redirect('home')

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
def MenuPlantas(request):
    plantas = Planta.objects.all()
    arbustos = Planta.objects.filter(categoria='Arbusto',archivada='False')
    arboles = Planta.objects.filter(categoria='Arbol',archivada='False')
    tipos_plantas = Planta.objects.filter(archivada='False').count()
    peso_total = Planta.objects.filter(archivada='False').aggregate(total_peso=Sum(F('peso') * F('stock')))['total_peso']
    cantidad_total = Planta.objects.filter(archivada='False').aggregate(Sum('stock'))['stock__sum']
    return render(request,'menu_plantas.html',{'plantas':plantas,'arbustos':arbustos,'arboles':arboles,'peso_total':peso_total,'cantidad_total':cantidad_total,'tipos_plantas':tipos_plantas})

@login_required    
def EliminarPlanta(request,id):
        planta = Planta.objects.filter(pk=id).first()
        if request.method == 'GET':
            return render(request,'eliminar_planta.html',{'planta':planta})
        else:
            planta.archivada = True
            planta.save()
            return redirect('menu_plantas')

@login_required
def crear_planta(request):
    if request.method == 'POST':
        form = CrearPlantaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menu_plantas')
        else:
            print(form.errors)
    else:
        form = CrearPlantaForm()
    return render(request, 'crear_planta.html', {'form': form})

@login_required
def modificar_planta(request, id):
    planta = Planta.objects.get(pk=id)  # Obtén la instancia de Planta a editar
    if request.method == 'POST':
        form = PlantaForm(request.POST, request.FILES, instance=planta)  # Pasa la instancia para editar
        if form.is_valid():
            form.save()
            return redirect('menu_plantas')
        else:
            print(form.errors)
    else:
        form = PlantaForm(instance=planta)  # Pasa la instancia para cargar los datos
        return render(request, 'editar_planta.html', {'form': form, 'planta': planta})

@login_required
def PlantasBorradas(request):
        plantas = Planta.objects.filter(archivada='True')
        return render(request,'plantas_eliminadas.html',{'plantas':plantas})
  
@login_required
def ReponerPlanta(request,id):
    try:
        planta = Planta.objects.filter(pk=id).first()
        if request.method=='GET':
            return render(request,'reponer_planta.html',{'planta':planta})
        else:
            planta.archivada = False
            planta.save()
            return redirect('menu_plantas')
    except:
        print("Ocurrio un problema al Encontrar la planta")








