from django.db import models
from django.contrib.auth.models import AbstractUser #Importa el modelo base de USUARIO de DJANGO
import json

# Create your models here.
#HACER MIGRACIONES CON MODIFICACIONES DE LOS MODELOS

#*-----USUARIO-----*
#Este modelo ya viene con: username, first_name, last_name, email, password, is_staff, is_active, date_joined, last_login
class Usuario(AbstractUser):
    fotografia = models.ImageField(upload_to='usuarios/', null=True, blank=True)
    telefono = models.CharField(max_length=20)
    fecha_de_nacimiento = models.DateField()
    direccion = models.CharField(max_length=100)
    
    #Verificacion del usuario
    fotografia_identificacion = models.ImageField(upload_to='identificaciones/', null=True, blank=True)
    verificado = models.BooleanField(default=False)
    
    #Bloqueos
    usuarios_bloqueados = models.ManyToManyField('self', symmetrical=False, related_name='usuarios_bloqueadores')

    # Definir related_name para grupos y permisos
    groups = models.ManyToManyField('auth.Group', related_name='usuarios')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='usuarios')

    def __str__(self):
        usuario_data = {
            "nombre": self.username,
            "contrasena": self.password,
            "telefono": self.telefono,
            "fecha_de_nacimiento": self.fecha_de_nacimiento,
            "direccion": self.direccion
        }
        return json.dumps(usuario_data, indent=2)

#*-----MASCOTA-----*
class Mascota(models.Model):
    dueño = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    peso = models.FloatField(null=True, blank=True, validators=[
            MinValueValidator(0),  # El peso no puede ser menor que 0
            MaxValueValidator(150)  # El peso no puede ser mayor que 100
        ])
    SEXO_CHOICES = (
        ('M', 'Macho'),
        ('H', 'Hembra'),
    )
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    TAMAÑO_CHOICES = (
        ('XS', ' MuyPequeño'),
        ('S', 'Pequeño'),
        ('M', 'Mediano'),
        ('L', 'Grande'),
        ('XL', 'Gigante'),
    )
    tamaño = models.CharField(max_length=15, choices=TAMAÑO_CHOICES)
    descripcion = models.TextField()
    RAZA_CHOICES = (
        ('Bulldog francés', 'Bulldog francés'),
        ('Labrador retriever', 'Labrador retriever'),
        ('Golden retriever', 'Golden retriever'),
        ('Pastor alemán', 'Pastor alemán'),
        ('Caniche', 'Caniche'),
        ('Bulldog', 'Bulldog'),
        ('Rottweiler', 'Rottweiler'),
        ('Beagle', 'Beagle'),
        ('Salchicha', 'Salchicha'),
        ('Braco alemán de pelo corto', 'Braco alemán de pelo corto'),
        ('Corgi galés de Pembroke', 'Corgi galés de Pembroke'),
        ('Pastor australiano', 'Pastor australiano'),
        ('Yorkshire terrier', 'Yorkshire terrier'),
        ('Cavalier King Charles spaniel', 'Cavalier King Charles spaniel'),
        ('Doberman pinscher', 'Doberman pinscher'),
        ('Boxer', 'Boxer'),
        ('Schnauzer miniatura', 'Schnauzer miniatura'),
        ('Cane corso', 'Cane corso'),
        ('Gran danés', 'Gran danés'),
        ('Shih Tzu', 'Shih Tzu'),
        ('Husky siberiano', 'Husky siberiano'),
        ('Chihuahua', 'Chihuahua'),  # Raza agregada
        ('Solovino', 'Solovino'),  # Raza agregada
    )
    raza = models.CharField(max_length=100, choices=RAZA_CHOICES)
    
    tiene_cartilla = models.BooleanField()
    likes = models.ManyToManyField("self", symmetrical=False, related_name="liked_by", blank=True)
    
    def __str__(self):
        return self.nombre        

#*-----IMAGENES_MASCOTA-----*
class ImagenMascota(models.Model):
    mascota = models.OneToOneField(Mascota, on_delete=models.CASCADE)
    imagen_1 = models.ImageField(upload_to='mascota_imagenes/')
    imagen_2 = models.ImageField(upload_to='mascota_imagenes/')
    imagen_3 = models.ImageField(upload_to='mascota_imagenes/')
    imagen_4 = models.ImageField(upload_to='mascota_imagenes/')
    imagen_5 = models.ImageField(upload_to='mascota_imagenes/')
    imagen_6 = models.ImageField(upload_to='mascota_imagenes/')

    def __str__(self):
        return f'Imágenes de {self.mascota.nombre}'

#*-----PREFERENCIAS*-----
#Revisar y ajustar los campos en base decidamos nuestro formulario
class Preferencias(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, null=True)
    preferencia_tamaño = models.CharField(max_length=15, choices=Mascota.TAMAÑO_CHOICES)
    preferencia_raza = models.CharField(max_length=100)
    preferencia_edad_min = models.IntegerField()
    preferencia_edad_max = models.IntegerField()

#*-----MATCH-----*
class Match(models.Model):
    mascota1 = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='mascota1')
    mascota2 = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='mascota2')
    fecha_match = models.DateTimeField(auto_now_add=True)
    
    bloqueado = models.BooleanField(default=False)  # Nuevo campo

    def __str__(self):
        return f'Match entre {self.mascota1.nombre} y {self.mascota2.nombre}'

#*-----MENSAJES-----*
class Chat(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    remitente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='remitente')
    destinatario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='destinatario')
    mensaje = models.TextField()
    fecha_mensaje = models.DateTimeField(auto_now_add=True)
    
    bloqueado = models.BooleanField(default=False)  # Nuevo campo

    def __str__(self):
        return f'Mensaje de {self.remitente.nombre} para {self.destinatario.nombre} en el chat de {self.match}'

#-----REPORTES-----*
class Reportes(models.Model):
    reportador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reportes_realizados')
    usuario_reportado = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reportes_recibidos')
    motivo = models.TextField()
    fecha_reporte = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reporte de {self.reportador.username} a {self.usuario_reportado.username}'