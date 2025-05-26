from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.models import User


def public_home(request):
    return render(request,'public_home.html')

@login_required
def home(request):
    return render(request,'home.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(f"Intento de inicio de sesión: {username}")  # Depuración
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            print("credenciales correctas")        
            return redirect('home')
        else:
            print("Usuario o contraseña incorrectos.")  # Depuración
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return redirect('login')  # Agregar redirección en caso de error
    return render(request, 'registration/login.html')

def login_estudiante(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            # Busca al usuario por el correo electrónico
            
            user = User.objects.get(email=email)
            # Autentica usando el nombre de usuario del usuario encontrado
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            
    return render(request, 'registration/login_estudiante.html')

def salir(request):
    logout(request)
    return redirect('login')

def salir_estudiante(request):
    logout(request)
    return redirect('login_estudiante')

