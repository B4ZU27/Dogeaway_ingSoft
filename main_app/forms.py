from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Mascota, ImagenMascota, Preferencias

# -----USER LOGIN-----
class LoginForm(AuthenticationForm):
    class Meta:
        model = Usuario
        fields = ['email', 'password']

#-----USER SIGNUP-----*
class UserForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2', 'telefono', 'fecha_de_nacimiento', 'direccion']
        widgets = {
            'telefono': forms.TextInput(attrs={'placeholder': 'Ejemplo: (123) 456-7890'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Pues tu casa we'}),
            'fecha_de_nacimiento': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}),
        }
        labels = {
        'username': 'Nombre de usuario',
        'email': 'Correo electrónico',
        'password1': 'Contraseña',
        'password2': 'Confirmar contraseña',
        'telefono' : 'Telefono',
        'direccion': 'Direccion',
        'fecha_de_nacimiento': 'Fecha de nacimiento'
        }

#-----MASCOTA SIGNUP-----*
class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'peso', 'sexo', 'tamaño', 'descripcion', 'raza', 'tiene_cartilla']

#-----IMAGENES DE MASCOTA-----*
class ImagenMascotaForm(forms.ModelForm):
    class Meta:
        model = ImagenMascota
        fields = ['mascota', 'imagen_1', 'imagen_2', 'imagen_3', 'imagen_4', 'imagen_5', 'imagen_6']

#-----TEST DE PREFERENCIAS-----*
class PreferenciasForm(forms.ModelForm):
    class Meta:
        model = Preferencias
        fields = ['mascota', 'preferencia_tamaño', 'preferencia_raza', 'preferencia_edad_min', 'preferencia_edad_max']