from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate,login
from usuario.forms import *
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

def RegistroUsuario(request,user_id=None):
    if user_id:
        user = get_object_or_404(User, pk=user_id)
        form = CustomUserChangeForm(instance=user)
        modo = 'Editar Usuario'
    else:
        user = None
        form = CustomUserCreationForm()
        modo = 'Registrar Usuario'

    if request.method == 'POST':
        if user:
            form = CustomUserChangeForm(request.POST, instance=user)
        else:
            form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            if not user.pk:  # Si es un nuevo usuario
                user.set_password(form.cleaned_data['password1'])  # Establece la contraseña si es un nuevo usuario
            user.save()

            # Asignar el grupo al usuario
            group = form.cleaned_data['group']
            user.groups.set([group])  # Establecer el grupo del usuario

            return redirect('appNuevoUsuario')


    return render(request, 'registration/register.html', {'form':form,'modo':modo})

def RegistroUsuarioExterno(request):
    
    user = None
    form = CustomUserCreationFormExternal()
    modo = 'Regístrate'

    if request.method == 'POST':

        form = CustomUserCreationFormExternal(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            if not user.pk:  # Si es un nuevo usuario
                user.set_password(form.cleaned_data['password1'])  # Establece la contraseña si es un nuevo usuario

            user.save()

            # Asignar el grupo al usuario
            group = Group.objects.get(id=2)
            user.groups.add(group)
            messages.success(request, 'Usuario registrado exitosamente y asignado al grupo.')


            return redirect('appNuevoUsuarioExterno')


    return render(request, 'registration/register_external.html', {'form':form,'modo':modo})

def CambiarPassword(request):
    if request.method == 'POST':
        id_usuario=request.POST.get('id_usuario')
        password=request.POST.get('password')
        print(id_usuario)
        print(password)
        user = get_object_or_404(User, id=id_usuario)
        user.set_password(password)
        user.save()
    return redirect ('appListarUsuario')


@login_required
@require_POST
def EliminarUsuario(request):
    id_usuario = request.POST.get('id_usuario_eliminar')
    user = get_object_or_404(User, id=id_usuario)
    # Nos asegúramos de que el usuario no pueda eliminarse a sí mismo
    if request.user == user:
        # Podrías mostrar un mensaje de error aquí
        return redirect('appListarUsuario')
    
    user.delete()
    return redirect('appListarUsuario')

def ListarUsuarios(request):
    usuarios = User.objects.all()
    return render(request,'gestionusuario/listarusuario.html',{'usuarios':usuarios})

def EditarUsuario(request):
    # usuarios = User.objects.all()
    return render(request,'gestionusuario/editarusuario.html')

def NuevoUsuario(request):
    return render(request,'gestionusuario/nuevousuario.html')