from django.db import models

class Vehiculo(models.Model):
    id = models.AutoField(primary_key=True)
    tipo_vehiculo = models.CharField(max_length=255)
    marca = models.CharField(max_length=255)
    modelo = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.marca} {self.modelo}"
