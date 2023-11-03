from apps.src.infra.models import Rol, Usuario, Vehiculo, ZonaComunes
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

from typing import List
class UsuarioAll:

    @staticmethod
    def agregar_rol(nombre):
        try:
            rol = Rol.objects.create(nombre=nombre)
            return rol
        except:
            raise Exception(f"Ya existe el rol {nombre}")
        
    @staticmethod
    def agregar_rol_al_usuario(id_rol,cedula):
        usuario = get_object_or_404(Usuario, cedula=cedula)
        nuevo_rol = get_object_or_404(Rol, id=id_rol)
        usuario.rol = nuevo_rol
        usuario.save()

        

    @staticmethod
    def registrar_usuario(email, password, rol_id, nombre, apellido, celular, cedula, edad, direccion, barrio, tipo_persona):
        if Usuario.objects.filter(email=email).exists():
            raise ValueError("Un usuario con este email ya está registrado.")
        print(rol_id)
        rol = Rol.objects.get(id=rol_id)
        
        usuario = Usuario.objects.create_user(
            email=email,
            password=password, 
            rol=rol,
            nombre=nombre,
            apellido=apellido,
            celular=celular,
            cedula=cedula,
            edad=edad,
            direccion=direccion,
            barrio=barrio,
            tipo_persona=tipo_persona
        )

        return usuario
    
    @staticmethod
    def obtener_usuario(email, password)->Usuario:
        return UsuarioAll.iniciar(email, password,sesion=False)
       
    @staticmethod
    def listar_roles():
        roles = Rol.objects.all()
        return [{"id": rol.id, "nombre": rol.nombre} for rol in roles]
        

    @staticmethod
    def agregar_vehiculo(tipo_vehiculo, marca, modelo):
        vehiculo = Vehiculo.objects.create(
            tipo_vehiculo=tipo_vehiculo,
            marca=marca,
            modelo=modelo
        )
        return vehiculo

    @staticmethod
    def agregar_zona_comun(nombre, maxHora, esDeposito, esPrecio, maxPersona, precio=None):
        zona_comun = ZonaComunes.objects.create(
            nombre=nombre,
            maxHora=maxHora,
            esDeposito=esDeposito,
            esPrecio=esPrecio,
            maxPersona=maxPersona,
            precio=precio
        )
        return zona_comun
    
    @staticmethod
    def listar_zona_comun():
        zona_comunes = ZonaComunes.objects.all()
        return zona_comunes

    
    
    @staticmethod
    def iniciar(email,password,sesion =True):
        try:
            usuario = Usuario.objects.filter(email=email).first()
            if not sesion:
                return usuario
            if usuario and usuario.check_password(password):
                refresh = RefreshToken.for_user(usuario)
                return {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    "usuario":usuario.id
                }
            else:
                raise Exception("Credenciales incorrectas")
        except Usuario.DoesNotExist:
            raise Exception("Correo no existe")