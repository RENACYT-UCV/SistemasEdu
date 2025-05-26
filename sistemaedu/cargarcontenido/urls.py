from .views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("cargarcontenido/index/", (index), name="cargarcontenido.index"),
    path("cargarcontenido/resumen/create", (resumen_create), name="resumen.create"),
    path("cargarcontenido/resumen/store", (resumen_store), name="resumen.store"),
    path("cargarcontenido/resumen/edit/<id>", (resumen_edit), name="resumen.edit"),
    path("cargarcontenido/resumen/update", (resumen_update), name="resumen.update"),

    path("cargarcontenido/documento/create", (documento_create), name="documento.create"),
    path("cargarcontenido/documento/store", (documento_store), name="documento.store"),
    path("cargarcontenido/documento/edit/<id>", (documento_edit), name="documento.edit"),
    path("cargarcontenido/documento/update", (documento_update), name="documento.update"),

    path("cargarcontenido/video/create", (video_create), name="video.create"),
    path("cargarcontenido/video/store", (video_store), name="video.store"),
    path("cargarcontenido/video/update", (video_update), name="video.update"),
    path("cargarcontenido/video/edit/<id_video>", (video_edit), name="video.edit"),
    path("cargarcontenido/video/delete/<id_video>", (video_delete), name="video.delete"),

]

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)