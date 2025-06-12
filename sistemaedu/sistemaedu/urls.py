"""sistemaedu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

from django.views.generic import TemplateView

#Cambio
from home.views import login, login_estudiante
###fin del cambio

urlpatterns = [
    path('', TemplateView.as_view(template_name='public_home.html'), name='public_home'),  # Esta es la página principal
    path('login/', include('home.urls')),  # Redirigir a /login
    path('', include('home.urls')),
    path('', include('cargarcontenido.urls')),
    path('', include('usuario.urls')),
    path('', include('gestionarcontenido.urls')),
    path('', include('estadistica.urls')),
    path('', include('contenidoalumno.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), #new



#    # Ruta para el login del estudiante 
#     path('login_estudiante/', TemplateView.as_view(template_name='registration/login_estudiante.html'), name='login_estudiante'),
# #  # Ruta para el login del admin 
#     path('login_admin/', TemplateView.as_view(template_name='registration/login.html'), name='admin_login'),

# 

####CAMBIOS###
path('login_estudiante/', login_estudiante, name='login_estudiante'),  

path('login_admin/', login, name='admin_login'),  # importar login de home.views

]
