from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views 
#------------------

urlpatterns = [
    path('', views.index, name = 'home'),

    path('login/', views.user_login, name='login'),
    path('verificacion/', views.verificacion, name='verificacion'),
    path('signup/', views.signup, name='signup'),

    path('lista/', views.ListaUsuariosView.as_view(), name='lista de usuarios'),

    path('preferencias/', views.preferencias, name='preferencias'),
    path('mascotas/registro/', views.registro_mascota, name='registro_mascota'),
    
    path('mascotas/<int:mascota_id>/cargar-imagenes/', views.cargar_imagenes_mascota, name='cargar_imagenes_mascota'),
    path('mascotas/', views.mascotas_usuario, name='mascotas_usuario'),
    
    path('usuario/<int:pk>/actualizar/', views.UsuarioUpdateView.as_view(), name='usuario_actualizar'),
    path('usuario/<int:pk>/eliminar/', views.UsuarioDeleteView.as_view(), name='usuario_eliminar'),
    path('usuario/<int:pk>/detalles/', views.UsuarioDetailView.as_view(), name='usuario_detalles'),

    
    path('mascota/<int:pk>/actualizar/', views.MascotaUpdateView.as_view(), name='mascota_actualizar'),
    path('mascota/<int:pk>/eliminar/', views.MascotaDeleteView.as_view(), name='mascota_eliminar'),
    path('mascota/detalles/', views.MascotaDetailView.as_view(), name='mascota_detalles'),
    
    path('chat/<int:match_id>/', views.chat_view, name='chat'),
    
    path('reportar/<int:usuario_id>/', views.reportar_usuario, name='reportar_usuario'),
    path('bloquear/<int:usuario_id>/', views.bloquear_usuario, name='bloquear_usuario'),
    path('desbloquear/<int:usuario_id>/', views.desbloquear_usuario, name='desbloquear_usuario'),
    path('usuarios_bloqueados/', views.lista_usuarios_bloqueados, name='lista_usuarios_bloqueados'),

    path('MATCH/', views.match_view, name='Match'),
    path('MATCH/like_mascota/', views.like_mascota, name='like_mascota'),

    path('logout/', LogoutView.as_view(), name='logout'),
]
