from django.urls import path
from estadistica.views import *

urlpatterns = [
    path("estadistica/index/", index, name="appestadistica.index"),
    path("datos/reproducciones/", datos_reproducciones, name="appdatos_reproducciones"),
    path("datos/registrar-reproduccion/<int:id>/", registrar_reproduccion, name="appdatos_registrar_reproduccion"),
]