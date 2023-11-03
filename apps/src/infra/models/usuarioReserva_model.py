from django.db import models
from apps.src.infra.models.reservas_model import Reservas
from apps.src.infra.models.usuario_model import Usuario

class UsuariosReservas(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='usuario_reservas')
    reserva = models.ForeignKey(Reservas, on_delete=models.CASCADE, related_name='usuario_reservas')
    date = models.DateField()
    horaEntrada = models.TimeField()
    bool = models.BooleanField(default=False, verbose_name="Estado")  # He añadido un nombre descriptivo para el campo
    esLlego = models.BooleanField(default=False)

    def __str__(self):
        return f"Detalle de {self.usuario.nombre} para la reserva {self.reserva.id} - Fecha: {self.date}"
