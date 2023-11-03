from django.db import models

class ZonaComunes(models.Model):
    id = models.AutoField(primary_key=True)
    esDisponible = models.BooleanField(default=True)
    nombre = models.CharField(max_length=255)
    maxHora = models.PositiveIntegerField(help_text="Número máximo de horas que se puede reservar")
    esDeposito = models.BooleanField(default=False, help_text="Indica si se requiere un depósito para reservar")
    esPrecio = models.BooleanField(default=False, help_text="Indica si tiene un precio asociado para su uso")
    maxPersona = models.PositiveIntegerField(help_text="Número máximo de personas permitidas")
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Precio de la zona común si esPrecio es verdadero")

    def __str__(self):
        return f"{self.nombre} - Disponible: {self.esDisponible}"