from django.urls import path
from usuario.views import *
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('register/',RegistroUsuario, name='register'),
    path('listar/usuario/',ListarUsuarios, name='appListarUsuario'), 
    path('nuevo/usuario/',RegistroUsuario, name='appNuevoUsuario'),
    path('eliminar/usuario/',EliminarUsuario, name='appEliminarUsuario'),
    path('nuevo/usuario/externo',RegistroUsuarioExterno, name='appNuevoUsuarioExterno'),
    path('actualizar/usuario/<user_id>/', RegistroUsuario, name='appEditarUsuario'),
    path('cambiar/password/',CambiarPassword, name='appCambiarPassword'),


     path('registration/password_reset/', PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html'),
        name='app_password_reset_form'),

    path('login/password_reset_done/', PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'),
        name='app_password_reset_done'),

    path('login/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'),
        name='app_password_reset_confirm'),

    path('login/reset/done/', PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'),
        name='app_password_reset_complete'),
]