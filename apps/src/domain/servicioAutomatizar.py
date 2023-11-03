
from apps.src.infra.models import Inmueble, UsuarioApartamentos


class ServicioAutomatizar:
    def __init__(self) -> None:
        pass
    
    def agregar_inmueble(tipo_inmueble, numero, piso=None, coeficiente=1.0, apartamento_dependiente_id=None):
        inmueble = Inmueble.objects.create(
            tipo_inmueble=tipo_inmueble,
            numero=numero,
            piso=piso,
            coeficiente=coeficiente,
            apartamento_dependiente_id=apartamento_dependiente_id
        )
        return inmueble
    
    def agregar_usuario_apartamento(self,usuario_id, inmueble_id, is_autorizado=False, is_dueño=True, coeficiente=1.0):
        relacion = UsuarioApartamentos.objects.create(
            usuario_id=usuario_id,
            inmueble_id=inmueble_id,
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
