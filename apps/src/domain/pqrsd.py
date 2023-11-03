from apps.src.infra.models.usuario_model import Usuario
from apps.src.infra.models.pqrsd_model import PQRSD
from apps.src.infra.models.comentario_model import Comentarios


class ServicePQRS:
    
    def __init__(self) -> None:
        pass
    
    def registrar_pqrsd(self,usuario_afectado_id, tipo_pqrs, cedula, edad, isCorreo, mensaje, evidencias):
        usuario = Usuario.objects.get(id=usuario_afectado_id)
        
        pqrsd = PQRSD.objects.create(
            usuario_afectado=usuario,
            tipo_pqrs=tipo_pqrs,
            cedula=cedula,
            edad=edad,
            isCorreo=isCorreo,
            mensaje=mensaje,
            evidencias=evidencias
        )
        return pqrsd
    
    def asignar_responsable(self,pqrsd_id, responsable_id):
        pqrsd = PQRSD.objects.get(id=pqrsd_id)
        responsable = Usuario.objects.get(id=responsable_id)
        if responsable.rol.nombre.lower() != "administrador":
            raise Exception("Debe ser admin")
        pqrsd.idResponsable = responsable
        pqrsd.save()
        
    def agregar_comentario(self,usuario_afectado_id, usuario_responsable_id, pqrsd_id, mensaje):
        usuario_afectado = Usuario.objects.get(id=usuario_afectado_id)
        usuario_responsable = Usuario.objects.get(id=usuario_responsable_id)
        pqrsd = PQRSD.objects.get(id=pqrsd_id)
        
        comentario = Comentarios.objects.create(
            usuario_afectado=usuario_afectado,
            usuario_responsable=usuario_responsable,
            pqrsd=pqrsd,
            mensaje=mensaje
        )
        return comentario
    
    
    def finalizar_pqrsd(self,pqrsd_id):
        pqrsd = PQRSD.objects.get(id=pqrsd_id)
        pqrsd.isEstado = True
        pqrsd.save()
        
    
    def listado_pqrsd_admin(self):
        pqrsds = PQRSD.objects.all()
        lista = []
        
        for pqrsd in pqrsds:
            lista.append({
                "id": pqrsd.id,
                "usuario": f"{pqrsd.usuario_afectado.nombre}",
                "fecha_registro": pqrsd.fecha_registro,
                "tipo_pqrs": pqrsd.get_tipo_pqrs_display(),
                "estado": "Finalizado" if pqrsd.isEstado else "Pendiente",
                "mensaje": pqrsd.mensaje,
                "responsable": pqrsd.idResponsable.nombre if pqrsd.idResponsable else None
            })
        return lista