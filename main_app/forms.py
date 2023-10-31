from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario, Mascota

class LoginForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['correo', 'contrasena']
        
class RegistroForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'correo', 'contrasena', 'telefono', 'fecha_de_nacimiento', 'direccion']

class RegistroMascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['dueño', 'nombre', 'peso', 'sexo', 'tamaño', 'descripcion', 'raza', 'tiene_cartilla']