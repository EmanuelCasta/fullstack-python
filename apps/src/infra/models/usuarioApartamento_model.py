from django.db import models
from apps.src.infra.models.inmueble_model import Inmueble
from apps.src.infra.models.usuario_model import Usuario

class UsuarioApartamentos(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='usuario_apartamentos')
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name='inmueble_usuarios')
    isAutorizado = models.BooleanField(default=False)
    isDueño = models.BooleanField(default=True)
    coeficiente = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Usuario: {self.usuario.nombre} - Inmueble: {self.inmueble.numeroApartamento} - Autorizado: {self.isAutorizado}"