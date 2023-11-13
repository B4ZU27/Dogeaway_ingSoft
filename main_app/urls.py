from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views 
#------------------

urlpatterns = [
    path('', views.index, name = 'Home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('lista/', views.ListaUsuariosView.as_view(), name='lista de usuarios'),
    path('preferencias/', views.preferencias, name='preferencias'),
    path('mascotas/registro/', views.registro_mascota, name='registro_mascota'),
    path('mascotas/<int:mascota_id>/cargar-imagenes/', views.cargar_imagenes_mascota, name='cargar_imagenes_mascota'),
    path('mascotas/', views.mascotas_usuario, name='mascotas_usuario'),
    path('home/', views.home, name='home'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
