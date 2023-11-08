from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views 
#------------------

urlpatterns = [
    path('', views.index, name = 'Home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('registro_mascota/', views.registro_mascota, name='registro de mascota'),
    path('lista/', views.ListaUsuariosView.as_view(), name='lista de usuarios'),
    path('preferencias/', views.preferencias_view, name='preferencias'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
