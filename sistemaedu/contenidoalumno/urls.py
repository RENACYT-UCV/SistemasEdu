from contenidoalumno.views import *
from django.urls import path

urlpatterns = [
    path("contenidoalumnos/videos/", contenido_videos, name="appcontenidovideos"),
    path("contenidoalumnos/documentos/", contenido_documentos, name="appcontenidodocumentos"),
    path("contenidoalumnos/textos/", contenido_textos, name="appcontenidotextos"),
    path("registrarreproduccion/", registrarreproduccion, name="appregistrarreproduccion"),
    
]

