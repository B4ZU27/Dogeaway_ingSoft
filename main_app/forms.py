from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Mascota, ImagenMascota, Preferencias, Reportes

# -----USER LOGIN-----
class LoginForm(AuthenticationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Correo electrónico:'}),
            'password': forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Contraseña:'}),
        }

#-----USER SIGNUP-----*
class UserForm(UserCreationForm):
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Contraseña:'})
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Confirmar contraseña:'})
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2', 'telefono', 'fecha_de_nacimiento', 'direccion']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Nombre completo:'}),
            'email': forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'Correo electrónico:'}),
            'telefono': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Ejemplo: (123) 456-7890'}),
            'direccion': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Direccion:'}),
            'fecha_de_nacimiento': forms.DateInput(attrs={'class': 'input-field', 'placeholder': 'YYYY-MM-DD'}),
        }
        labels = {
            'username': 'Nombre completo',
            'email': 'Correo electrónico',
            'telefono': 'Telefono',
            'direccion': 'Direccion',
            'fecha_de_nacimiento': 'Fecha de nacimiento',
        }

#-----VERIFICACION-----*
class VerificacionForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['fotografia_identificacion']
        labels = {
            'fotografia_identificacion': 'Subir foto de identificación',
        }
        widgets = {
            'fotografia_identificacion': forms.ClearableFileInput(attrs={'class': 'input-field'}),
        }

#-----MASCOTA SIGNUP-----*
class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'peso', 'sexo', 'tamaño', 'descripcion', 'raza', 'tiene_cartilla']
        labels = {
            'tiene_cartilla': '¿Tiene cartilla de vacunación?',
            'nombre': 'Nombre',
        }


#-----IMAGENES DE MASCOTA-----*
class ImagenMascotaForm(forms.ModelForm):
    class Meta:
        model = ImagenMascota
        fields = ['imagen_1', 'imagen_2', 'imagen_3', 'imagen_4', 'imagen_5', 'imagen_6']
    def clean(self):
        cleaned_data = super().clean()
        num_imagenes_llenas = sum(1 for field_name in self.fields if cleaned_data.get(field_name) is not None)
        
        if num_imagenes_llenas >= 2:
            # Marcamos el formulario como válido
            self.cleaned_data['is_valid'] = True
        else:
            # Marcamos el formulario como no válido
            self.add_error(None, "Se requieren al menos dos imágenes.")
            self.cleaned_data['is_valid'] = False

        return self.cleaned_data


#-----TEST DE PREFERENCIAS-----*
class PreferenciasForm(forms.ModelForm):
    class Meta:
        model = Preferencias
        fields = ['preferencia_tamaño', 'preferencia_raza', 'preferencia_edad_min', 'preferencia_edad_max']

#-----REPORTES FORM-----*
class ReportesForm(forms.ModelForm):
    class Meta:
        model = Reportes
        fields = ['motivo']
