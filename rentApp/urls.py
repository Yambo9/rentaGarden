from rentaPlant.urls import *
from django.contrib import admin
from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('',Home,name='home'),
    path('register/',Register,name='register'),
    path('logout/',Logout,name='logout'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)