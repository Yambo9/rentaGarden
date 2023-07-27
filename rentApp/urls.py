from rentaPlant.urls import *
from django.contrib import admin
from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('',Home,name='home'),
    path('register/',Register,name='register'),
    path('signin/',Signin,name='signin'),
    path('logout/',Logout,name='logout'),
    path('profile/',Profile,name='profile'),
    path('crear_arrendatario/',Crear_arrendatario,name="crear_arrendatario"),
    path('catalogo/',Catalogo,name='catalogo'),
    path('detalle_planta/<int:id>/', DetallePlanta, name='detalle_planta'),
    path('menu_pedidos/', menuArriendo, name='menuArriendo'),


    path('menu_ejecutivos/', MenuEjecutivos, name='menu_ejecutivos'),
    path('crear_ejecutivo/', CrearEjecutivo, name='crear_ejecutivo'),






]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)