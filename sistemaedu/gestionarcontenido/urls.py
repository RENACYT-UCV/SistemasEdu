from django.urls import path
from gestionarcontenido.views import *
urlpatterns = [
    path("gestionarcontenido/index", gestionarcontenido_index, name="gestionarcontenido.index"),
    path("gestionarcontenido/procesar/video/<id>", procesar_video, name="procesar.video"),
    path("gestionarcontenido/procesar/resumen/<id>", procesar_resumen, name="procesar.resumen"),
    path("gestionarcontenido/procesar/documento/<id>", procesar_documento, name="procesar.documento"),
]
