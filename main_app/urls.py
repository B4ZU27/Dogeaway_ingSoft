from django.urls import path
from . import views 
#------------------

urlpatterns = [
    path('', views.index),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('registro_mascota/', views.registro_mascota, name='registro de mascota'),
    path('lista/', views.ListaUsuariosView.as_view(), name='lista de usuarios'),
    #path('preferencias/', views.preferencias, name='preferencias')
]
