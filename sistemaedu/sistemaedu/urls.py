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


####CAMBIOS###
path('login_estudiante/', login_estudiante, name='login_estudiante'),  

path('login_admin/', login, name='admin_login'),  # importar login de home.views

]
