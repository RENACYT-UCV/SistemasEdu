from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required
urlpatterns = [
    #path('', login_required(index),name='home'),
    path('public_home', public_home,name='public_home'),
    path('home', login_required(home),name='home'),
    path('login', login, name='login'),
    path("login_estudiante/", login_estudiante, name="login_estudiante"),
    path('salir/', salir,name='salir'),
    path('salirestudiante/', salir_estudiante,name='salir_estudiante')
]