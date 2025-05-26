from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

import os

class Documento(models.Model):
    nombre = models.CharField(max_length=255)
    archivo = models.CharField(max_length=255)
    contenido_texto=models.TextField(default='-')
    resumen_ai = models.TextField(default='-')

    def __str__(self):
        self.nombre
    
    def get_documento_url(self):
        return os.path.join(settings.MEDIA_URL, self.archivo)

class Resumen(models.Model):
    nombre = models.CharField(max_length=255)
    resumen = models.TextField(default='-')
    resumen_ai = models.TextField(default='-')

    def __str__(self):
        self.nombre

class Video(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(default='-')
    video = models.CharField(max_length=255)
    video_resumen=models.CharField(max_length=255)
    audio = models.CharField(max_length=255,default='-')
    texto = models.TextField(default='-')
    texto_resumen = models.TextField(default='-')
    reproducciones = models.PositiveIntegerField(default=0)
    genera_alumno=models.BooleanField(default=False)
    def __str__(self):
        self.nombre

    def get_video_url(self):
        return os.path.join(settings.MEDIA_URL, self.video)
    
    def get_video_resumen_url(self):
        return os.path.join(settings.MEDIA_URL,'resumenes', self.video_resumen)
    def get_audio_url(self):
        return os.path.join(settings.MEDIA_URL, self.audio)
    
class VideoReproduccion(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_reproduccion = models.DateTimeField(auto_now_add=True)