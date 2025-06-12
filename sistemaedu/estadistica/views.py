from django.shortcuts import render
#from cargarcontenido.models import *
from django.http import JsonResponse
from django.db import connection

def index(request):
    return render(request,'estadistica/index.html')

def datos_reproducciones(request):
   from django.shortcuts import render
from django.http import JsonResponse
from cargarcontenido.models import Video
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

def index(request):
    return render(request, 'estadistica/index.html')

def datos_reproducciones(request):
    videos = Video.objects.all()
    datos = [{"nombre": v.nombre, "reproducciones": float(v.reproducciones)} for v in videos]
    return JsonResponse({'reproducciones': datos})

@csrf_exempt
def registrar_reproduccion(request, id):
    if request.method == 'POST':
        try:
            video = Video.objects.get(id=id)
            video.reproducciones += 1
            video.save()
            return JsonResponse({'status': 'ok', 'reproducciones': video.reproducciones})
        except Video.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Video no encontrado'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)