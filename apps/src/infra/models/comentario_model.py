from django.db import models
from apps.src.infra.models.usuario_model import Usuario
from apps.src.infra.models.pqrsd_model import PQRSD



class Comentarios(models.Model):
    id = models.AutoField(primary_key=True)
    usuario_afectado = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='comentarios_afectado')
    usuario_responsable = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='comentarios_responsable')
    pqrsd = models.ForeignKey(PQRSD, on_delete=models.CASCADE, related_name='comentarios')
    mensaje = models.TextField()
    isVisto = models.BooleanField(default=False)
    FechaMensaje = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.usuario_afectado.nombre} sobre PQRSD {self.pqrsd.id} - Fecha: {self.FechaMensaje.date()}"
