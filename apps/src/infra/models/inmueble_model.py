from django.db import models

class Inmueble(models.Model):
    TIPO_INMUEBLE_CHOICES = [
        ('Apartamento', 'Apartamento'),
        ('Parqueadero', 'Parqueadero'),
        ('CuartoÚtil', 'Cuarto Útil')
    ]
    id = models.AutoField(primary_key=True)
    tipo_inmueble = models.CharField(max_length=255, choices=TIPO_INMUEBLE_CHOICES)
    numero = models.CharField(max_length=255)
    piso = models.IntegerField(null=True, blank=True)  
    coeficiente = models.DecimalField(max_digits=5, decimal_places=2)
    apartamento_dependiente = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)  
    
    def __str__(self):
        return f"{self.tipo_inmueble} {self.numero}"
