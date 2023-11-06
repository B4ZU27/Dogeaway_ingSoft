from django.urls import path
from . import views 
#------------------
from .views import ListaUsuariosView

urlpatterns = [
    path('home/', views.index),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('registro_mascota/', views.registro_mascota, name='registro_mascota'),
    path('lista_usuario/', ListaUsuariosView.as_view(), name='lista_usuarios'),
    path('lista_de_usuarios/', views.lista_usuarios, name='lista_usuario'),
    #path('preferencias/', views.preferencias, name='preferencias')
]
