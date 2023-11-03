from django.db import models
from apps.src.infra.models.vehiculo_model import Vehiculo
from apps.src.infra.models.usuario_model import Usuario

class VehiculoUsuario(models.Model):
    id = models.AutoField(primary_key=True)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='vehiculo_usuarios')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='vehiculo_usuarios')
    placa = models.CharField(max_length=20)
    isDueño = models.BooleanField(default=True)
    numeroParqueadero = models.CharField(max_length=20)

    def __str__(self):
        return f"Usuario: {self.usuario.nombre} - Vehículo: {self.vehiculo.marca} {self.vehiculo.modelo} - Placa: {self.placa}"