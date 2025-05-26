from django.shortcuts import render,redirect, get_object_or_404
from cargarcontenido.models import *
from django.conf import settings
import os
from django.core.files.storage import FileSystemStorage
from .forms import VideoForm
from datetime import datetime
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login as auth_login


def index(request):
    resumenes= Resumen.objects.all()
    documentos=Documento.objects.all()
    videos=Video.objects.all()
    return render(request, 'cargarcontenido/index.html',context={
        'documentos':documentos,'resumenes':resumenes,'videos':videos
    })

def documento_create(request):
    return render(request, 'cargarcontenido/documento_create.html')

def resumen_create(request):
    return render(request, 'cargarcontenido/resumen_create.html')

def video_create(request):
    return render(request,'cargarcontenido/video_create.html')

def video_store(request):
    if request.method == 'POST' and request.FILES.get('video'):
        nombre = request.POST.get('nombre')
        genera_alumno = request.POST.get('genera_alumno')
        descripcion = request.POST.get('descripcion')
        myfile = request.FILES['video']

        now = datetime.now()
        datetime_str = now.strftime("%Y%m%d%H%M%S")
        original_filename = myfile.name
        filename_pre = original_filename.split('.')[0]
        extension = original_filename.split('.')[-1]
        unique_filename = f"{filename_pre}_{datetime_str}.{extension}"

        fs = FileSystemStorage()
        filename = fs.save(unique_filename, myfile)
        uploaded_file_url = fs.url(filename)

        obj = Video()
        obj.nombre = nombre
        obj.descripcion = descripcion
        obj.video = unique_filename
        
        user = request.user  # Utiliza el usuario autenticado

        # Verifica la pertenencia a los grupos
        if user.groups.filter(name='Admin').exists():
            obj.genera_alumno = genera_alumno
        else:
            obj.genera_alumno = False

        obj.save()
        return redirect('cargarcontenido.index')
    
    # Agregar lógica para manejar solicitudes GET o casos donde no se suba un archivo
    return render(request, 'template_name.html')  # R

def video_edit(request,id_video):
    video = Video.objects.get(id=id_video)
    return render(request,'cargarcontenido/video_edit.html',{'video':video})

def video_update(request):
    id_video=request.POST.get('id_video')
    nombre=request.POST.get('nombre')
    video=request.FILES.get('video')
    descripcion =request.POST.get('descripcion')
    genera_alumno=request.POST.get('genera_alumno')
    if request.method=='POST':
        obj=Video.objects.get(id=id_video)

        if video:
            myfile=request.FILES['video']

            now = datetime.now()
            datetime_str = now.strftime("%Y%m%d%H%M%S")
            original_filename = myfile.name
            filename_pre=original_filename.split('.')[0]
            extension = original_filename.split('.')[-1]
            unique_filename = filename_pre+"_"+datetime_str+"."+extension

            fs=FileSystemStorage()
            filename=fs.save(unique_filename,myfile)
            uploaded_file_url=fs.url(filename)#la url del archivo cargado
            
            obj.video=unique_filename
        
        obj.nombre=nombre
        obj.descripcion=descripcion

        user = request.user  # Utiliza el usuario autenticado

        # Verifica la pertenencia a los grupos
        if user.groups.filter(name='Admin').exists():
            obj.genera_alumno = genera_alumno
        else:
            obj.genera_alumno = False


        obj.save()
        return redirect('cargarcontenido.index')

def video_delete(request,id_video):
    video = Video.objects.get(id=id_video)
    video.delete()
    return redirect('cargarcontenido.index') 
    

def resumen_store(request):
    nombre=request.POST.get('nombre')
    resumen=request.POST.get('resumen')
    obj=Resumen()
    obj.nombre=nombre
    obj.resumen=resumen
    obj.save()

    return redirect('cargarcontenido.index')

def resumen_update(request):
    id_resumen=request.POST.get('id_resumen')
    nombre=request.POST.get('nombre')
    resumen=request.POST.get('resumen')
    resumen_ai=request.POST.get('resumen_ai')
    obj=Resumen.objects.get(id=id_resumen)
    obj.nombre=nombre
    obj.resumen=resumen
    obj.resumen_ai=resumen_ai
    obj.save()
    return redirect('cargarcontenido.index')

def resumen_edit(request,id):
    resumen=Resumen.objects.get(id=id)
    return render(request,'cargarcontenido/resumen_edit.html',{'resumen':resumen})


def documento_store(request):
    nombre=request.POST.get('nombre')
    archivo=request.FILES.get('archivo')
    now = datetime.now()

    if request.method=='POST' and request.FILES['archivo']:
        myfile=request.FILES['archivo']
        fs=FileSystemStorage()
        filename=fs.save(myfile.name,myfile)
        uploaded_file_url=fs.url(filename)
        
        obj=Documento()
        obj.nombre=nombre
        obj.archivo=archivo
        obj.save()

    return redirect('cargarcontenido.index')
    
def documento_edit(request,id):
    documento=Documento.objects.get(id=id)
    return render(request,'cargarcontenido/documento_edit.html',{'documento':documento})

def documento_update(request):
    id_documento=request.POST.get('id_documento')
    nombre=request.POST.get('nombre')
    archivo=request.FILES.get('archivo')
    now = datetime.now()

    if request.method=='POST':
        obj=Documento.objects.get(id=id_documento)
        
        myfile=request.FILES['archivo']
        fs=FileSystemStorage()
        
        if request.FILES['archivo']:
            documento_borrar=os.path.join(settings.MEDIA_ROOT, obj.archivo)
            if os.path.exists(documento_borrar):
                os.remove(documento_borrar)
                print("borrado....")
    
        filename=fs.save(myfile.name,myfile)
        uploaded_file_url=fs.url(filename)
        
        obj.nombre=nombre
        obj.archivo=archivo
        obj.resumen_ai='-'
        obj.contenido_texto='-'
        obj.save()

    return redirect('cargarcontenido.index')
    

