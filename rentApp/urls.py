from rentaPlant.urls import *
from django.contrib import admin
from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[

    #PAGINA GENERAL
    path('',Home,name='home'),
    path('crear_arrendatario/',Crear_arrendatario,name="crear_arrendatario"),
    path('catalogo/',Catalogo,name='catalogo'),
    path('detalle_planta/<int:id>/', DetallePlanta, name='detalle_planta'),

    # FUNCIONES USUARIO
    path('register/',Register,name='register'),
    path('signin/',Signin,name='signin'),
    path('logout/',Logout,name='logout'),
    path('profile/',Profile,name='profile'),

    #MENSAJE ANONIMO DE USUARIOS
    path('mensaje/',Mensaje_Anonimo,name='mensaje_anonimo'),

    #MANEJO DE MENSAJES DEL ADMIN
    path('menu_mensajes/',Menu_mensajes,name='menu_mensajes'),
    path('leer_mensaje/<int:id>/',Leer_mensaje,name='leer_mensaje'),

    #LOGICA PEDIDO
    path('seleccionar_plantas/',seleccionar_plantas_pedido,name='seleccionar_plantas'),
    path('detalle_seleccion_plantas/<int:id>/',detalle_seleccion_plantas,name='detalle_seleccion_plantas'),
    path('eliminar_seleccion/<int:id>/',Eliminar_seleccion,name='eliminar_seleccion'),
    path('direccion_pedido/',Direccion_pedido,name='direccion_pedido'),


    #MANEJO DE PLANTAS DE PARTE DEL ADMIN
    path('crear_planta/', crear_planta, name='crear_planta'),
    path('menu_plantas/',MenuPlantas,name='menu_plantas'),
    path('modificar_planta/<int:id>/',modificar_planta,name='modificar_planta'),
    path('eliminar_planta/<int:id>/',EliminarPlanta,name='eliminar_planta'),
    path('plantas_eliminadas/',PlantasBorradas,name='plantas_eliminadas'),
    path('reponer_plantas.html/<int:id>/',ReponerPlanta,name='reponer_planta'),

    #LOGICA EJECUTIVOS
    path('menu_ejecutivos/', MenuEjecutivos, name='menu_ejecutivos'),
    path('crear_ejecutivo/', CrearEjecutivo, name='crear_ejecutivo'),
    path('eliminar_ejecutivo/<int:id>/', EliminarEjecutivo, name='eliminar_ejecutivo'),
    path('modificar_ejecutivo/<int:id>/', ModificarEjecutivo, name='modificar_ejecutivo'),






]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)