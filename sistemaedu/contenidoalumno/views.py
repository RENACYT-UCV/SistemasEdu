from django.shortcuts import render
from cargarcontenido.models import *
from django.http import JsonResponse


def contenido_videos(request):
    videos= Video.objects.all()
    return render(request,'contenidoalumno/videos.html',{'videos':videos})

def contenido_documentos(request):
    documentos= Documento.objects.all()
    return render(request,'contenidoalumno/documentos.html',{'documentos':documentos})

def contenido_textos(request):
    textos= Resumen.objects.all()
    return render(request,'contenidoalumno/textos.html',{'textos':textos})

def registrarreproduccion(request):
    if request.method == 'POST':
        video_id = request.POST['video_id']
        print(video_id)
        if video_id:
            video = Video.objects.get(id=video_id)
            VideoReproduccion.objects.create(video=video, usuario=request.user)
            video.reproducciones += 1
            video.save()
            return JsonResponse({'message': 'Reproducción registrada exitosamente'})
    return JsonResponse({'error': 'Solicitud inválida'}, status=400)
