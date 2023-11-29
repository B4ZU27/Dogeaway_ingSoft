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
            'fecha_de_nacimiento': forms.DateInput(attrs={'class': 'input-field', 'placeholder': 'Fecha de nacimiento: '}),
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
        fields = ['nombre','edad', 'peso', 'sexo', 'tamaño', 'descripcion', 'raza', 'tiene_cartilla', 'adopcion']
        labels = {
            'tiene_cartilla': '¿Tiene cartilla de vacunación?',
            'adopcion': '¿Esta mascota está en adopcion?',
            'nombre': 'Nombre',
            'edad': 'Edad',
            'peso':'Peso en Kg'
        }

# -----IMAGENES DE MASCOTA-----
class ImagenMascotaForm(forms.ModelForm):
    class Meta:
        model = ImagenMascota
        fields = ['imagen_1', 'imagen_2', 'imagen_3', 'imagen_4', 'imagen_5', 'imagen_6']

    def __init__(self, *args, **kwargs):
        super(ImagenMascotaForm, self).__init__(*args, **kwargs)
        self.fields['imagen_1'].required = False
        self.fields['imagen_2'].required = False
        self.fields['imagen_3'].required = False
        self.fields['imagen_4'].required = False
        self.fields['imagen_5'].required = False
        self.fields['imagen_6'].required = False

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
      
#-----EDITAR USUARIO FORM-----*
class UserEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'telefono', 'fecha_de_nacimiento', 'direccion']
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

#-----EDITAR MASCOTA FORM-----*
class MascotaEditForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'peso', 'edad', 'sexo', 'tamaño', 'raza', 'tiene_cartilla', 'descripcion']


#-----TEST DE PREFERENCIAS-----*
class PreferenciasForm(forms.ModelForm):
    class Meta:
        model = Preferencias
        fields = ['preferencia_tamaño', 'preferencia_raza', 'preferencia_edad_min', 'preferencia_edad_max']
        labels = {
            'preferencia_tamaño': 'Tamaño de la mascota',
            'preferencia_raza': 'Raza de preferencia',
            'preferencia_edad_min': 'Edad mínima preferida',
            'preferencia_edad_max': 'Edad máxima preferida',
        }
        help_texts = {
            'preferencia_tamaño': 'Selecciona el tamaño deseado para tu mascota.',
            'preferencia_raza': 'Indica la raza de preferencia para tu mascota.',
            'preferencia_edad_min': 'Ingresa la edad mínima preferida para tu mascota.',
            'preferencia_edad_max': 'Ingresa la edad máxima preferida para tu mascota.',
        }
        widgets = {
            'preferencia_tamaño': forms.Select(choices=Mascota.TAMAÑO_CHOICES),
            'preferencia_raza': forms.Select(choices=Mascota.RAZA_CHOICES),
        }

#-----REDES SOCIALES FORM-----*
class MascotaRedesSocialesForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['facebook_mascota', 'twitter_mascota', 'instagram_mascota', 'tiktok_mascota']
        labels = {
            'facebook_mascota': 'Facebook URL',
            'twitter_mascota': 'Twitter URL',
            'instagram_mascota': 'Instagram URL',
            'tiktok_mascota': 'TikTok URL',
        }
        widgets = {
            'facebook_mascota': forms.URLInput(attrs={'placeholder': 'https://www.facebook.com/'}),
            'twitter_mascota': forms.URLInput(attrs={'placeholder': 'https://twitter.com/'}),
            'instagram_mascota': forms.URLInput(attrs={'placeholder': 'https://www.instagram.com/'}),
            'tiktok_mascota': forms.URLInput(attrs={'placeholder': 'https://www.tiktok.com/@username'}),
        }

#-----REPORTES FORM-----*
class ReportesForm(forms.ModelForm):
    class Meta:
        model = Reportes
        fields = ['motivo']
