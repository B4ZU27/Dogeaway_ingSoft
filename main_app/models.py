from django.db import models

# Create your models here.
#te dejo poner aqui todas las tablas que se necesiten mauro
class Mascota(models.Model):
    name = models.CharField(maxlength = 20)