from django.db import models
from apps.src.infra.models.usuario_model import Usuario
from apps.src.infra.models.inmueble_model import Inmueble
from apps.src.infra.models.vehiculo_model import Vehiculo

class RegistroVisitante(models.Model):
    fecha_hora_ingreso = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='registros_visitantes')
    tipo_identificacion = models.CharField(max_length=255)
    numero_identificacion = models.CharField(max_length=20, unique=True)
    telefono_contacto = models.CharField(max_length=20)
    apartamento = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name='registros_visitantes')
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='registros_visitantes', null=True, blank=True)
    numero_parqueadero = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.usuario.nombre} - Fecha de ingreso: {self.fecha_hora_ingreso}"
