from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views 
#------------------

urlpatterns = [
    path('', views.index, name = 'home'),

        #Login/Signup
    path('login/', views.user_login, name='login'),
    path('verificacion/', views.verificacion, name='verificacion'),
    path('codigo-verificacion/', views.codigo_verificacion, name='codigo_verificacion'),
    path('signup/', views.signup, name='signup'),

    path('lista/', views.ListaUsuariosView.as_view(), name='lista de usuarios'),

        #Signup Mascota y Preferencias
    path('preferencias/', views.preferencias, name='preferencias'),
    path('editar_preferencias/', views.editar_preferencias, name='editar_preferencias'),
    path('mascotas/registro/', views.registro_mascota, name='registro_mascota'),
    path('mascotas/subir-imagenes/<int:mascota_id>/', views.subir_imagenes_mascota, name='subir_imagenes_mascota'),
    
        #Img Mascota y Elegir Mascota
    path('mascotas/', views.mascotas_usuario, name='mascotas_usuario'),
    
        #CRUD Usuario
    path('ver_informacion/', views.VerInformacionUsuario.as_view(), name='ver_informacion_usuario'),
    path('actualizar_informacion/', views.ActualizarInformacionUsuario, name='actualizar_informacion_usuario'),
    path('eliminar_cuenta/', views.EliminarCuentaUsuario.as_view(), name='eliminar_cuenta_usuario'),
    
        #CRUD Mascota
    path('ver_detalle_mascota/<int:mascota_id>/', views.VerDetalleMascota.as_view(), name='ver_detalle_mascota'),
    path('editar_mascota/<int:mascota_id>/', views.ActualizarInformacionMascota, name='editar_mascota'),
    path('editar_redes_sociales/<int:mascota_id>/', views.editar_redes_sociales, name='editar_redes_sociales'),
    path('eliminar_mascota/<int:mascota_id>/', views.EliminarMascota.as_view(), name='eliminar_mascota'),
    
        #Chat
    path('chat/<int:match_id>/', views.chat_view, name='chat'),
    
        #Reportes y Bloqueos
    path('reportar/<int:usuario_id>/', views.reportar_usuario, name='reportar_usuario'),
    path('bloquear/<int:usuario_id>/', views.bloquear_usuario, name='bloquear_usuario'),
    path('desbloquear/<int:usuario_id>/', views.desbloquear_usuario, name='desbloquear_usuario'),
    path('usuarios_bloqueados/', views.lista_usuarios_bloqueados, name='lista_usuarios_bloqueados'),

        #Match
    path('MATCH/', views.match_view, name='Match'),
    path('MATCH/like_mascota/', views.like_mascota, name='like_mascota'),

        #Logout
    path('logout/', LogoutView.as_view(), name='logout'),
]
