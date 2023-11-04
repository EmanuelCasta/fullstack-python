from datetime import datetime, timedelta
from apps.src.infra.models.usuario_model import Usuario
from apps.src.infra.models.zonasComunes_model import ZonaComunes
from apps.src.infra.models.reservas_model import Reservas
from apps.src.infra.models.usuarioReserva_model import UsuariosReservas
import pytz
from django.db import transaction

class ReservaService:
    
    def __init__(self) -> None:
        pass
    
    def realizar_reserva(self,usuario_id, zona_comun_id, hora_entrada, hora_salida, invitados=[]):
     
  
    
    
        usuario = Usuario.objects.get(id=usuario_id)
        zona_comun = ZonaComunes.objects.get(id=zona_comun_id)
        
        local_timezone = pytz.timezone("America/Bogota")
        now_with_timezone = datetime.now(local_timezone)

        if hora_entrada.date() < now_with_timezone.date() or  hora_salida.date() < now_with_timezone.date() :
            raise Exception("La fecha de reserva no puede ser anterior al día de hoy.")
        
        if  hora_salida.date() < hora_entrada.date():
            raise Exception("La fecha de salida debe ser mayor a la de entrada.")

        
        if not invitados:
            raise Exception("No hay ningun invitado.")
        
        if not zona_comun.esDisponible:
            raise Exception("La zona común no está disponible para reserva.")
        
    
        if usuario.edad < 18:
            raise Exception("El residente debe ser mayor de edad para realizar una reserva.")
        
     
        duracion_reserva = (hora_salida - hora_entrada).seconds // 3600
        if duracion_reserva > zona_comun.maxHora:
            raise Exception(f"No se puede reservar por más de {zona_comun.maxHora} horas.")
        
     
        if len(invitados) > zona_comun.maxPersona:
            raise Exception(f"No se puede reservar para más de {zona_comun.maxPersona} personas.")
        
        reservas_solapadas = Reservas.objects.filter(
            zona_comun=zona_comun,
            horaDeEntrada__lt=hora_salida,  
            horaDeSalida__gt=hora_entrada   
        )

        if reservas_solapadas.exists():
            raise Exception("Ya existe una reserva en la fecha y hora solicitadas para esta zona común.")
        
        self.validar_reglas_zona_comun(zona_comun_id, hora_entrada, duracion_reserva)
       
        with transaction.atomic():
            reserva = Reservas.objects.create(
                zona_comun=zona_comun,
                usuario=usuario,
                horaDeEntrada=hora_entrada,
                horaDeSalida=hora_salida,
                cantidadPersonas=len(invitados),
                precio=zona_comun.precio if zona_comun.esPrecio else 0,
                deposito=zona_comun.precio if zona_comun.esDeposito else 0
            )
            cedula_inv= 0
            try:
                for cedula_invitado in invitados:
                        cedula_inv =cedula_invitado
                        usuario_invitado = Usuario.objects.get(cedula=cedula_invitado)
                        
                        UsuariosReservas.objects.create(
                            usuario=usuario_invitado,
                            reserva=reserva,
                            date=hora_entrada.date(),
                            horaEntrada=hora_entrada.time()
                        )
            except Usuario.DoesNotExist:
                   
                    raise  Exception(f"No se encontró un usuario con la cédula {cedula_inv}.")


        return reserva
    
    def cancelar_reserva(self,reserva_id):
        reserva = Reservas.objects.get(id=reserva_id)
        
        local_timezone = pytz.timezone("America/Bogota")
        now_with_timezone = datetime.now(local_timezone)
        tiempo_restante = reserva.horaDeEntrada - now_with_timezone

        
        if tiempo_restante.total_seconds() < 7200:
            raise Exception("La cancelación debe realizarse al menos 2 horas antes de la hora de inicio de la reserva o no llego nadie a la reserva.")

        reserva.esCancelado = True
        reserva.save()
    
    def obtener_reservas_por_zona(self,zona_comun_id):
        return Reservas.objects.filter(zona_comun_id=zona_comun_id, esCancelado=False).order_by('-createReserva')

    def verificar_disponibilidad(self,zona_comun_id, hora_entrada, hora_salida):
        reservas = Reservas.objects.filter(
            zona_comun_id=zona_comun_id,
            esCancelado=False,
            horaDeEntrada__lt=hora_salida,
            horaDeSalida__gt=hora_entrada
        )
        return not reservas.exists()


    def listado_para_encargados(self, usuario_id):
        local_timezone = pytz.timezone("America/Bogota")
        now_with_timezone = datetime.now(local_timezone)
        
        reservas = Reservas.objects.filter(esCancelado=False, horaDeEntrada__gt=now_with_timezone).select_related('zona_comun', 'usuario').order_by('-createReserva')
        
        listado = []
        for reserva in reservas:
            listado.append({
                'Apartamento': reserva.usuario.id,
                'Responsable': f"{reserva.usuario.nombre} {reserva.usuario.apellido}",
                'FechaInicio': reserva.horaDeEntrada,
                'FechaFin': reserva.horaDeSalida,
                'ReciboPago': reserva.IsPago,
                'DepositoEntregado': reserva.isDeposito
            })
        return listado

    def listado_para_porteria(self, usuario_id):
        local_timezone = pytz.timezone("America/Bogota")
        now_with_timezone = datetime.now(local_timezone)

        reservas = Reservas.objects.filter(esCancelado=False, horaDeEntrada__gt=now_with_timezone).select_related('zona_comun', 'usuario').order_by('-createReserva')
        
        listado = []
        for reserva in reservas:
            invitados = UsuariosReservas.objects.filter(reserva=reserva)
            listado_invitados = [f"{invitado.usuario.nombre} {invitado.usuario.apellido}" for invitado in invitados]

            listado.append({
                'Apartamento': reserva.usuario.id,
                'Responsable': f"{reserva.usuario.nombre} {reserva.usuario.apellido}",
                'FechaInicio': reserva.horaDeEntrada,
                'FechaFin': reserva.horaDeSalida,
                'ReciboPago': reserva.IsPago,
                'DepositoEntregado': reserva.isDeposito,
                'Invitados': ",".join(listado_invitados)
            })
        print(listado_invitados,"Hila!")
        return listado

    

    def validar_reglas_zona_comun(self,zona_comun_id, hora_entrada, duracion):
        zona = ZonaComunes.objects.get(id=zona_comun_id)
        hoy = datetime.now().date()
        hora_actual = datetime.now().time()
        fecha_entrada = hora_entrada.date()

        if zona.nombre == "Salón Social":
            if fecha_entrada == hoy and hora_entrada.time() <= hora_actual:
                raise ValueError("No se puede reservar para una hora pasada el mismo día.")
            if (hora_entrada.time().hour < 8) or ((hora_entrada + timedelta(hours=duracion)).time().hour > 22 and fecha_entrada.weekday() < 5) or ((hora_entrada + timedelta(hours=duracion)).time().hour > 24 and fecha_entrada.weekday() == 5) or ((hora_entrada + timedelta(hours=duracion)).time().hour > 22 and fecha_entrada.weekday() == 6):
                raise ValueError("Horario de reserva fuera del permitido para el Salón Social.")
            if duracion > 7 or duracion < 2:
                raise ValueError("La duración debe ser entre 2 y 7 horas.")
            

        elif zona.nombre == "Zona BBQ":
            if duracion > 4:
                raise ValueError("La duración máxima para la Zona BBQ es de 4 horas.")

        elif zona.nombre == "Cancha Sintética":
            if duracion > 2:
                raise ValueError("La duración máxima para la Cancha Sintética es de 2 horas.")
            if hora_entrada.time().hour < 8 or hora_entrada.time().hour > 22:
                raise ValueError("Horario de reserva fuera del permitido para la Cancha Sintética.")

        elif zona.nombre == "Zona Húmeda":
            if duracion > 2:
                raise ValueError("La duración máxima para la Zona Húmeda es de 2 horas.")
            if hora_entrada.time().hour < 9 or hora_entrada.time().hour > 17:
                raise ValueError("Horario de reserva fuera del permitido para la Zona Húmeda.")
            
