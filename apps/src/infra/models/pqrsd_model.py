from django.db import models
from apps.src.infra.models.usuario_model import Usuario


class PQRSD(models.Model):
    id = models.AutoField(primary_key=True)
    usuario_afectado  = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pqrsd_usuario')
    fecha_registro = models.DateField(auto_now_add=True)
    TIPOS_PQRS = [
        ('P', 'Petición'),
        ('Q', 'Queja'),
        ('R', 'Reclamo'),
        ('S', 'Sugerencia'),
        ('D', 'Denuncia')
    ]
    tipo_pqrs = models.CharField(max_length=1, choices=TIPOS_PQRS, default='P')
    cedula = models.CharField(max_length=20)
    edad = models.PositiveIntegerField()
    isCorreo = models.BooleanField(default=False)
    isEstado = models.BooleanField(default=False)
    idResponsable = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='pqrsd_responsable')
    mensaje = models.TextField()
    evidencias = models.FileField(upload_to='evidencias_pqrsd/')

    def __str__(self):
        return f"PQRSD de {self.usuario_afectado.nombre} - Tipo: {self.get_tipo_pqrs_display()} - Fecha: {self.fecha_registro}"
