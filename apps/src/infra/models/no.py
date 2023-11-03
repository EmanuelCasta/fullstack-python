from django.db import models
class Nos(models.Model):
    id = models.AutoField(primary_key=True)
    numeroApartamento = models.CharField(max_length=255)