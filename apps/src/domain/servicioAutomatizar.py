
from apps.src.infra.models import Inmueble, UsuarioApartamentos
from apps.src.infra.models.usuario_model import Usuario
from django.shortcuts import get_object_or_404

class ServicioAutomatizar:
    def __init__(self) -> None:
        pass
    
    def agregar_inmueble(self,tipo_inmueble, numero,code, piso=None, coeficiente=1.0):

        inmueble = Inmueble.objects.create(
            tipo_inmueble=tipo_inmueble,
            numero=numero,
            piso=piso,
            coeficiente=coeficiente,
            code =code
        )
        return inmueble
    
    def agregar_usuario_apartamento(self,cedula, inmueble_id, is_autorizado=False, is_dueño=True, coeficiente=1.0):
        usuario = get_object_or_404(Usuario, cedula=cedula)
        inmueble = get_object_or_404(Inmueble, code=inmueble_id)
        relacion = UsuarioApartamentos.objects.create(
            usuario=usuario,
            inmueble=inmueble,
            isAutorizado=is_autorizado,
            isDueño=is_dueño,
            coeficiente=coeficiente
        )
        return relacion
    
    def listar_inmuebles_con_detalles(self):
        inmuebles = Inmueble.objects.prefetch_related('inmueble_usuarios__usuario__vehiculo_usuarios__vehiculo').all()

        detalles = []

        for inmueble in inmuebles:
            info = {
                "inmueble": inmueble.numero,
                "tipo": inmueble.tipo_inmueble,
                "piso": inmueble.piso,
                "residentes": [],
            }
            for relacion in inmueble.inmueble_usuarios.all():
                vehiculos = [{"marca": vehiculo.vehiculo.marca, "modelo": vehiculo.vehiculo.modelo, "placa": vehiculo.placa} for vehiculo in relacion.usuario.vehiculo_usuarios.all()]
                residente = {
                    "nombre": relacion.usuario.nombre,
                    "apellido": relacion.usuario.apellido,
                    "es_dueño": relacion.isDueño,
                    "vehiculos": vehiculos
                }
                info["residentes"].append(residente)
            detalles.append(info)

        return detalles
