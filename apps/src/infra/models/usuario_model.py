from django.db import models
from apps.src.infra.models.rol_model import Rol
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):
    def _create_user(self, email, nombre, apellido, password=None, is_staff=False, is_superuser=False, **extra_fields):
        if not email:
            raise ValueError('El campo email es requerido')
        if not nombre:
            raise ValueError('El campo nombre es requerido')
        if not apellido:
            raise ValueError('El campo apellido es requerido')
        
        user = self.model(
            email=self.normalize_email(email),
            nombre=nombre,
            apellido=apellido,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, nombre, apellido, password=None, **extra_fields):
        return self._create_user(email, nombre, apellido, password, False, False, **extra_fields)

    def create_superuser(self, email, nombre, apellido, password=None, **extra_fields):
        return self._create_user(email, nombre, apellido, password, True, True, **extra_fields)

    
    
class Usuario(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, related_name='usuarios',null=True)
    nombre = models.CharField(max_length=255)
    apellido= models.CharField(max_length=255)
    celular = models.CharField(max_length=20)
    cedula = models.CharField(max_length=20, unique=True) 
    edad = models.PositiveIntegerField(null=True)
    email = models.EmailField(max_length=255, unique=True) 
    direccion = models.TextField(null=True)
    barrio = models.CharField(max_length=255)
    tipo_persona = models.CharField(max_length=255)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre','apellido']

    
    def __str__(self):
        return f"{self.nombre} - {self.cedula}"