import json
from django.db import models

# Create your models here.
#HACER MIGRACIONES CON MODIFICACIONES DE LOS MODELOS

#*-----USUARIO-----*
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100)
    contrasena = models.CharField(max_length=100)
    fotografia = models.ImageField(upload_to='usuarios/', null=True, blank=True)
    telefono = models.CharField(max_length=20)
    fecha_de_nacimiento = models.DateField()
    direccion = models.CharField(max_length=100)
    verificacion = models.BooleanField()

    def __str__(self):
        usuario_data = {
            "nombre": self.nombre,
            "contrasena": self.contrasena,
            "telefono": self.telefono,
            "fecha_de_nacimiento": self.fecha_de_nacimiento,
            "direccion": self.direccion
        }
        return json.dumps(usuario_data, indent=2)

#*-----MASCOTA-----*
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
    tiene_cartilla = models.BooleanField() #¿No deberia ser una imagen de la cartilla?
    #¿Eliminar los siguientes ya con la creacion de la clase MATCH?
    likes = models.ManyToManyField("self", symmetrical=False, related_name="liked_by", blank=True)
    matches = models.ManyToManyField("self", symmetrical=False, related_name="matched_with", blank=True)
    
    def __str__(self):
        return self.nombre        

#*-----IMAGENES_MASCOTA-----*
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

#*-----MATCH-----*
class Match(models.Model):
    mascota1 = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='mascota1')
    mascota2 = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='mascota2')
    fecha_match = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Match entre {self.mascota1.nombre} y {self.mascota2.nombre}'

#*-----MENSAJES-----*
class Chat(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    remitente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='remitente')
    destinatario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='destinatario')
    mensaje = models.TextField()
    fecha_mensaje = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Mensaje de {self.remitente.nombre} para {self.destinatario.nombre} en el chat de {self.match}'