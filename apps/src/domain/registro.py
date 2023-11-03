from apps.src.infra.models.usuario_model import Usuario
from apps.src.infra.models.usuarioApartamento_model import UsuarioApartamentos
from apps.src.infra.models.inmueble_model import Inmueble
from apps.src.infra.models.vehiculoUsuario_model import VehiculoUsuario
from apps.src.infra.models.registroVisitantes_model import RegistroVisitante

class RegistroVisitantes:
    def __init__(self) -> None:
        pass
    def autorizar_ingreso(self,apartamento_id, visitante_id):
        try:
            autorizacion = UsuarioApartamentos.objects.get(inmueble__id=apartamento_id, usuario__id=visitante_id, isAutorizado=True)
            if autorizacion:
                return True
            else:
                raise Exception("El residente no ha autorizado el ingreso del visitante.")
        except UsuarioApartamentos.DoesNotExist:
            raise Exception("No se encontró una autorización para este visitante.")
        
    def registrar_visitante(self, usuario_id, tipo_identificacion, numero_identificacion, telefono_contacto, apartamento_id, vehiculo_usuario_id=None, numero_parqueadero=None):
        usuario = Usuario.objects.get(id=usuario_id)
        apartamento = Inmueble.objects.get(id=apartamento_id)
        vehiculo_usuario = VehiculoUsuario.objects.get(id=vehiculo_usuario_id) if vehiculo_usuario_id else None
        
        if not self.autorizar_ingreso(apartamento_id, usuario_id):
            raise Exception("El ingreso del visitante no está autorizado.")
        
        registro = RegistroVisitante.objects.create(
            usuario=usuario,
            tipo_identificacion=tipo_identificacion,
            numero_identificacion=numero_identificacion,
            telefono_contacto=telefono_contacto,
            apartamento=apartamento,
            vehiculo_usuario=vehiculo_usuario,
            numero_parqueadero=numero_parqueadero
        )
        return registro

    
    def lista_vigilantes(self):
        autorizaciones = UsuarioApartamentos.objects.filter(isAutorizado=True)
        lista = []
        for autorizacion in autorizaciones:
            lista.append({
                "apartamento": f"{autorizacion.inmueble.numeroApartamento} - {autorizacion.inmueble.piso}",
                "residente_nombre": autorizacion.usuario.nombre,
                "residente_telefono": autorizacion.usuario.celular
            })
        return lista
    
    def autorizar_residente(self,usuario_id, apartamento_id):
        try:
            autorizacion = UsuarioApartamentos.objects.get(usuario__id=usuario_id, inmueble__id=apartamento_id)
            autorizacion.isAutorizado = True
            autorizacion.save()
        except UsuarioApartamentos.DoesNotExist:
            raise Exception("No se encontró el registro del residente en el apartamento indicado.")
