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
    path('crear_arrendatario/',Crear_arrendatario,name="crear_arrendatario")


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)