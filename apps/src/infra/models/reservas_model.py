from django.db import models
from apps.src.infra.models.zonasComunes_model import ZonaComunes
from apps.src.infra.models.usuario_model import Usuario



class Reservas(models.Model):
    id = models.AutoField(primary_key=True)
    zona_comun = models.ForeignKey(ZonaComunes, on_delete=models.CASCADE, related_name='reservas')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reservas')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    deposito = models.DecimalField(max_digits=10, decimal_places=2)
    cantidadPersonas = models.PositiveIntegerField()
    esCancelado = models.BooleanField(default=False)
    horaDeSalida = models.DateTimeField()
    horaDeEntrada = models.DateTimeField()
    createReserva = models.DateTimeField(auto_now_add=True)
    isDeposito = models.BooleanField(default=False, help_text="Indica si se ha realizado el depósito")
    IsPago = models.BooleanField(default=False, help_text="Indica si se ha realizado el pago")

    def __str__(self):
        return f"Reserva de {self.usuario.nombre} para {self.zona_comun.nombre} - Fecha: {self.createReserva.date()}"