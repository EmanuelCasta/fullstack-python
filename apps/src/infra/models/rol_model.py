from django.db import models

class Rol(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "rol"
        verbose_name_plural = "roles"

    def __str__(self):
        return self.nombre