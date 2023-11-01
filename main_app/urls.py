from django.urls import path
from . import views 

urlpatterns = [
    path('', views.hello),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('registro_mascota/', views.registro_mascota, name='registro_mascota')
]
