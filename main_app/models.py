import json
from django.db import models

# Create your models here.
#Aqui estaran las clases listadas por diego

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    contrasena = models.CharField(max_length=100)
    fotografia = models.ImageField(upload_to='usuarios/', null=True, blank=True)
    telefono = models.CharField(max_length=20)
    fecha_de_nacimiento = models.DateField()
    ubicacion = models.CharField(max_length=100)

    def __str__(self):
        usuario_data = {
            "nombre": self.nombre,
            "contrasena": self.contrasena,
            "telefono": self.telefono,
            "fecha_de_nacimiento": self.fecha_de_nacimiento,
            "ubicacion": self.ubicacion
        }
        return json.dumps(usuario_data, indent=2)

class Mascota(models.Model):
    dueño = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    peso = models.FloatField(null=True, blank=True)
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
    raza = models.CharField(max_length=100)
    tiene_cartilla = models.BooleanField()
    likes = models.ManyToManyField("self", symmetrical=False, related_name="liked_by", blank=True)
    matches = models.ManyToManyField("self", symmetrical=False, related_name="matched_with", blank=True)

    
    def __str__(self):
        return self.nombre        

class ImagenMascota(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    imagen_1 = models.ImageField(upload_to='mascota_imagenes/')
    imagen_2 = models.ImageField(upload_to='mascota_imagenes/')
    imagen_3 = models.ImageField(upload_to='mascota_imagenes/')
    imagen_4 = models.ImageField(upload_to='mascota_imagenes/')
    imagen_5 = models.ImageField(upload_to='mascota_imagenes/')
    imagen_6 = models.ImageField(upload_to='mascota_imagenes/')

    def __str__(self):
        return f'Imágenes de {self.mascota.nombre}'
