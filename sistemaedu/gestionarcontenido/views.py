from django.shortcuts import render
from cargarcontenido.models import *
from django.http import JsonResponse
from datetime import datetime
from moviepy.editor import VideoFileClip, concatenate_videoclips

from django.shortcuts import render
from django.http import JsonResponse
from .models import TextSummarizer

from docx import Document as DocxDocument
import speech_recognition as sr
import random

from transformers import pipeline


def gestionarcontenido_index(request):
    videos=Video.objects.all()
    resumenes=Resumen.objects.all()
    documentos=Documento.objects.all()
    return render(request,'gestionarcontenido/index.html',{'videos':videos,'resumenes':resumenes,'documentos':documentos})

def procesar_resumen(request,id):
    resumen = Resumen.objects.get(id=id)
    summarizer = TextSummarizer()
    summary = summarizer.summarize(resumen.resumen)
    resumen.resumen_ai=summary
    resumen.save()
    return JsonResponse({'message':'Resumen Generado Satisfactoriamente'})


def procesar_video(request,id):
    # try:
    now = datetime.now()
    datetime_str = now.strftime("%Y%m%d%H%M%S")
    
    video=Video.objects.get(id=id)

    #obtiene el video resumen si existe lo borra del directorio
    if video.video_resumen:
        video_borrar=os.path.join(settings.MEDIA_ROOT, 'resumenes', video.video_resumen)
        if os.path.exists(video_borrar):
            os.remove(video_borrar)

    #obtiene el video
    input_video_path = os.path.join(settings.MEDIA_ROOT, video.video)
    

    #obtiene el nombre del video
    nombrevideo=(video.video).split('.')[0]
    #obtiene extension del video
    extensionvideo=(video.video).split('.')[-1]
    #nombre del video
    unique_filename = nombrevideo+"_"+datetime_str+"."+extensionvideo
    
    
    #establece una ruta para video resumen
    output_video_path = os.path.join(settings.MEDIA_ROOT, 'resumenes', unique_filename)
    
    
    #crea el directorio si no existe
    os.makedirs(os.path.dirname(output_video_path), exist_ok=True)

    # procesar_video_resumen(input_video_path,output_video_path)

    #carga el video al VideoFileClip
    video_clip = VideoFileClip(input_video_path)
    
    # Obtiene la duración del video
    video_duration = video_clip.duration
    half_duration = video_duration / 2

    # Genera segmentos  que sumen al menos la mitad de la duración del video original
    total_segment_duration = 0
    segments = []
    
    while total_segment_duration < half_duration:
        cuts = sorted(random.sample(range(int(video_duration)), 4))
        segments = [(cuts[i], cuts[i+1]) for i in range(len(cuts)-1)]
        total_segment_duration = sum(end - start for start, end in segments)

    #cortamos los segmentos
    clips = [video_clip.subclip(start, end) for start, end in segments]

    #unimos los segmentos cortados en un solo video
    final_clip = concatenate_videoclips(clips)
    #guardamos el video resumen
    final_clip.write_videofile(output_video_path, codec='libx264')

    audio, texto=extraer_audio_y_convertir_a_texto(input_video_path)

    # Definir el modelo de resumen específico para español
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # Dividir el texto en segmentos si es muy largo
    max_tokens = 1024  # Este es un ejemplo, ajusta según el límite del modelo
    
    segments = [texto[i:i+max_tokens] for i in range(0, len(texto), max_tokens)]

    # Generar resúmenes para cada segmento
    summaries = [summarizer(segment, max_length=90, min_length=5, do_sample=False) for segment in segments]

    # Unir los resúmenes
    full_summary = " ".join([summary[0]['summary_text'] for summary in summaries])

    #summary=summarizer(texto,max_length=100,min_length=10,do_sample=False)

    #actualizamos en la tabla el nombre del archivo
    video.video_resumen = unique_filename
    video.audio=audio
    video.texto=texto
    video.texto_resumen=full_summary
    video.save()

    return JsonResponse({'message':'procesamiento exitoso'})
    # except  Exception as e:
    #     return JsonResponse({'data':str(e)})

def extraer_audio_y_convertir_a_texto(input_video_path):

    video_clip = VideoFileClip(input_video_path)
    output_audio_path = input_video_path.replace('.mp4', '.wav')
    video_clip.audio.write_audiofile(output_audio_path)
    audio_text = ""

    recognizer = sr.Recognizer()
    # Ajustar la sensibilidad del reconocedor de voz
    with sr.AudioFile(output_audio_path) as source:
        recognizer.adjust_for_ambient_noise(source)

    file_name = os.path.splitext(os.path.basename(output_audio_path))[0]
    file_extension = os.path.splitext(output_audio_path)[1]
    nombre_audio=file_name+file_extension
    
    


    try:
        with sr.AudioFile(output_audio_path) as source:
            audio_data = recognizer.record(source)
            audio_text = recognizer.recognize_google(audio_data,language='es-ES')
    # except Exception as e:
    #     audio_text = f"Error al convertir el audio a texto: {str(e)}"
    except sr.RequestError as e:
        audio_text = f"Error al conectar con el servicio de reconocimiento de voz: {str(e)}"
    except sr.UnknownValueError:
        audio_text = "No se pudo entender el audio."
    except Exception as e:
        audio_text = f"Error al convertir el audio a texto: {str(e)}"
    
    return nombre_audio, audio_text


# def procesar_video_resumen(input_video_path,output_video_path):
    


def procesar_documento(request,id):
    
    doc = Documento.objects.get(id=id)
    ruta_documento = os.path.join(settings.MEDIA_ROOT, doc.archivo)
    #cuando es Word
    docx_text = read_docx(ruta_documento)
    
    #cuando es pdf
    #pdf_text = read_pdf(ruta_documento)
    
    summarizer = TextSummarizer()
    summary = summarizer.summarize(docx_text)

    doc.contenido_texto=docx_text
    doc.resumen_ai = summary
    doc.save()
    return JsonResponse({'message':'Texto extraído con éxito'})


#Creamos una función para extraer el texto
def read_docx(file_path):
    
    doc = DocxDocument(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

