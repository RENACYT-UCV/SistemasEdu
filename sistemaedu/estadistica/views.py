from django.shortcuts import render
#from cargarcontenido.models import *
from django.http import JsonResponse
from django.db import connection

def index(request):
    return render(request,'estadistica/index.html')

def datos_reproducciones(request):
    with connection.cursor() as cursor:
        cursor.callproc('spReproducciones')
    
        resultados = cursor.fetchall()

        datos=[]

        for row in resultados:
            datos.append({
                            'nombre':row[0],
                            'reproducciones':float(row[1])
            })
    return JsonResponse({'reproducciones':datos})