from django.db import models
from apps.src.infra.models.pqrsd_model import PQRSD

class Documento(models.Model):
    id = models.AutoField(primary_key=True)
    pqrsd =  models.ForeignKey(PQRSD, on_delete=models.CASCADE, related_name='documento_afectado')
    nombre = models.CharField(max_length=255)
    archivo_pdf = models.BinaryField(blank=True, null=True)