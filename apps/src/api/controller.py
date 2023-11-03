def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': {
            'id': user.id,
            'email': user.email,
            'nombre': user.nombre
        }
    }
    
from rest_framework import serializers
from rest_framework.exceptions import APIException
class DynamicJsonSerializer(serializers.Serializer):
    data = serializers.JSONField()
import datetime
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from apps.src.domain.agregar import UsuarioAll
from apps.src.domain.pqrsd import ServicePQRS
from apps.src.domain.registro import RegistroVisitantes
from apps.src.domain.services import ReservaService
from apps.src.domain.servicioAutomatizar import ServicioAutomatizar

class UsuarioViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DynamicJsonSerializer

    @action(detail=False, methods=['POST'], permission_classes=[AllowAny],url_path='registrar')
    def registro(self, request):
        try:
            try:
                email = request.data.get("email")
                password = request.data.get("password")
                rol_id = request.data.get("rol_id")
                nombre = request.data.get("nombre")
                apellido = request.data.get("apellido")
                celular = request.data.get("celular")
                cedula = request.data.get("cedula")
                edad = request.data.get("edad")
                direccion = request.data.get("direccion")
                barrio = request.data.get("barrio")
                tipo_persona = request.data.get("tipo_persona")
                if not email or not password or not rol_id or not  nombre or not apellido or not celular or not cedula or not edad or not direccion or not barrio or not tipo_persona:
                    raise Exception()
                print("HOla")
            except:
                return Response({"message": str("Debes tener todos los campos")}, status=status.HTTP_400_BAD_REQUEST)
            UsuarioAll.registrar_usuario(email, password, rol_id, nombre, apellido, celular, cedula, edad, direccion, barrio, tipo_persona)
            usuario = UsuarioAll.iniciar(email, password)
            return Response(usuario)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], permission_classes=[AllowAny],url_path='iniciar')
    def login(self, request):
        try:
            email = request.data.get("email")
            password = request.data.get("password")
            usuario = UsuarioAll.iniciar(email, password)
            response = JsonResponse(usuario)
            response.set_cookie('token', usuario['access'])
            return response
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated], url_path='agregar-rol')
    def agregar_rol(self, request):
        try:
            try:
                nombre = request.data.get("nombre")
            except:
                nombre = request.data["nombre"]
            rol = UsuarioAll.agregar_rol(nombre)
            return Response({"rol_id": rol.id, "nombre": rol.nombre},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False,methods=["POST"],permission_classes=[IsAuthenticated],url_path="listar_roles")
    def listar_roles(self,request):
        roles = UsuarioAll.listar_roles()
        return Response(roles)
    
    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated], url_path='agregar-rol-al-usuario')
    def agregar_rol_al_usuario(self, request):
        try:
            cedula = request.data.get("cedula")
            id_rol  = request.data.get("id")
            rol = UsuarioAll.agregar_rol_al_usuario(id_rol,cedula)
            return Response({"message":"Exito!"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_400_BAD_REQUEST)
    
    
    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated], url_path='obtener-usuario')
    def obtener_usuario(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        
        usuario = UsuarioAll.obtener_usuario(email,password)
        return Response({"nombre":usuario.nombre,"rol":usuario.rol.nombre,"celular":usuario.celular,"correo":usuario.email,"barrios":usuario.barrio})

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated], url_path='agregar-vehiculo')
    def agregar_vehiculo(self, request):
        tipo_vehiculo = request.data.get("tipo_vehiculo")
        marca = request.data.get("marca")
        modelo = request.data.get("modelo")
        vehiculo = UsuarioAll.agregar_vehiculo(tipo_vehiculo, marca, modelo)
        return Response({"vehiculo_id": vehiculo.id, "marca": vehiculo.marca, "modelo": vehiculo.modelo})

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated], url_path='agregar-zona-comun')
    def agregar_zona_comun(self, request):
        nombre = request.data.get("nombre")
        maxHora = request.data.get("maxHora")
        esDeposito = request.data.get("esDeposito")
        esPrecio = request.data.get("esPrecio")
        maxPersona = request.data.get("maxPersona")
        precio = request.data.get("precio", None)
        zona_comun = UsuarioAll.agregar_zona_comun(nombre, maxHora, esDeposito, esPrecio, maxPersona, precio)
        return Response({
            "zona_comun_id": zona_comun.id,
            "nombre": zona_comun.nombre,
        })
        
    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated], url_path='listar-zona-comun')
    def listar_zona_comun(self,request):
        data = []
        zona_comunes = UsuarioAll.listar_zona_comun()
        for zona_comun in zona_comunes:
            data.append({
                "precio":zona_comun.precio,
                "esDeposito":zona_comun.esDeposito,
                "esDisponible":zona_comun.esDisponible,
                "esPrecio":zona_comun.esPrecio,
                "id":zona_comun.id,
                "maxPersonas":zona_comun.maxPersona,
                "maxHora":zona_comun.maxHora,
                "nombre":zona_comun.nombre
                })
        return Response(data)
        
class PQRSViewSet(viewsets.ViewSet):  
    permission_classes = [IsAuthenticated]
    serializer_class = DynamicJsonSerializer  

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated], url_path='registrar-pqrsd')
    def registrar_pqrsd(self, request):
        data = request.data
        usuario_afectado_id = data.get("usuario_afectado_id")
        tipo_pqrs = data.get("tipo_pqrs")
        cedula = data.get("cedula")
        edad = data.get("edad")
        isCorreo = data.get("isCorreo")
        mensaje = data.get("mensaje")
        evidencias = data.get("evidencias")
        
        result = ServicePQRS().registrar_pqrsd(usuario_afectado_id, tipo_pqrs, cedula, edad, isCorreo, mensaje, evidencias)
        return Response(result)

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated], url_path='asignar-responsable')
    def asignar_responsable(self, request, pk=None):
        pqrsd_id = pk
        responsable_id = request.data.get("responsable_id")
        
        result = ServicePQRS().asignar_responsable(pqrsd_id, responsable_id)
        return Response(result)

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated], url_path='agregar-comentario')
    def agregar_comentario(self, request):
        usuario_afectado_id = request.data.get("usuario_afectado_id")
        usuario_responsable_id = request.data.get("usuario_responsable_id")
        pqrsd_id = request.data.get("pqrsd_id")
        mensaje = request.data.get("mensaje")

        result = ServicePQRS().agregar_comentario(usuario_afectado_id, usuario_responsable_id, pqrsd_id, mensaje)
        return Response(result)

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated], url_path='finalizar-pqrsd')
    def finalizar_pqrsd(self, request, pk=None):
        pqrsd_id = pk

        result = ServicePQRS().finalizar_pqrsd(pqrsd_id)
        return Response(result)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated], url_path='listado-pqrsd-admin')
    def listado_pqrsd_admin(self, request):
        result = ServicePQRS().listado_pqrsd_admin()
        return Response(result)

class RegistroVisitantesViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DynamicJsonSerializer  

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated], url_path='autorizar-ingreso')
    def autorizar_ingreso(self, request):
        apartamento_id = request.data.get("apartamento_id")
        visitante_id = request.data.get("visitante_id")
        
        result = RegistroVisitantes().autorizar_ingreso(apartamento_id, visitante_id)
        return Response(result)

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated], url_path='registrar-visitante')
    def registrar_visitante(self, request):
        usuario_id = request.data.get("usuario_id")
        tipo_identificacion = request.data.get("tipo_identificacion")
        numero_identificacion = request.data.get("numero_identificacion")
        
        result = RegistroVisitantes().registrar_visitante(usuario_id, tipo_identificacion, numero_identificacion)
        return Response(result)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated], url_path='lista-vigilantes')
    def lista_vigilantes(self, request):
        result = RegistroVisitantes().lista_vigilantes()
        return Response(result)

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated], url_path='autorizar-residente')
    def autorizar_residente(self, request):
        usuario_id = request.data.get("usuario_id")
        apartamento_id = request.data.get("apartamento_id")
        
        result = RegistroVisitantes().autorizar_residente(usuario_id, apartamento_id)
        return Response(result)

class ReservaServiceViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DynamicJsonSerializer 

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated], url_path='realizar-reserva')
    def realizar_reserva(self, request):
        try:
            usuario_id = request.data.get("usuario_id")
            zona_comun_id = request.data.get("zona_comun_id")
            hora_entrada = request.data.get("hora_entrada")
            hora_salida = request.data.get("hora_salida")
            invitados = request.data.get("invitados", [])
        
            hora_entrada =datetime.datetime.fromisoformat(hora_entrada)
            hora_salida = datetime.datetime.fromisoformat(hora_salida)
            print("Aqui!!!!",invitados)
            
            result = ReservaService().realizar_reserva(usuario_id, zona_comun_id, hora_entrada, hora_salida, invitados)
            return Response({
                "message":"Reserva exitosa!!!"
            })
        except Exception as e:
            print(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated], url_path='cancelar-reserva')
    def cancelar_reserva(self, request):
        reserva_id = request.data.get("reserva_id")
        
        result = ReservaService().cancelar_reserva(reserva_id)
        return Response(result)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated], url_path='obtener-reservas-por-zona')
    def obtener_reservas_por_zona(self, request):
        zona_comun_id = request.query_params.get("zona_comun_id")
        result = ReservaService().obtener_reservas_por_zona(zona_comun_id)
        return Response(result)

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated], url_path='verificar-disponibilidad')
    def verificar_disponibilidad(self, request):
        zona_comun_id = request.data.get("zona_comun_id")
        hora_entrada = request.data.get("hora_entrada")
        hora_salida = request.data.get("hora_salida")
        
        result = ReservaService().verificar_disponibilidad(zona_comun_id, hora_entrada, hora_salida)
        return Response(result)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated], url_path='listado-para-encargados')
    def listado_para_encargados(self, request):
        usuario_id = request.query_params.get("usuario_id")
        result = ReservaService().listado_para_encargados(usuario_id)
        return Response(result)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated], url_path='listado-para-porteria')
    def listado_para_porteria(self, request):
        usuario_id = request.query_params.get("usuario_id")
        result = ReservaService().listado_para_porteria(usuario_id)
        return Response(result)

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated], url_path='validar-reglas-zona-comun')
    def validar_reglas_zona_comun(self, request):
        zona_comun_id = request.data.get("zona_comun_id")
        hora_entrada = request.data.get("hora_entrada")
        duracion = request.data.get("duracion")
        
        result = ReservaService().validar_reglas_zona_comun(zona_comun_id, hora_entrada, duracion)
        return Response(result)

class ServicioAutomatizarViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DynamicJsonSerializer  

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated], url_path='agregar-inmueble')
    def agregar_inmueble(self, request):
        tipo_inmueble = request.data.get("tipo_inmueble")
        numero = request.data.get("numero")
        piso = request.data.get("piso", None)
        coeficiente = request.data.get("coeficiente", 1.0)
        apartamento_dependiente_id = request.data.get("apartamento_dependiente_id", None)
        result = ServicioAutomatizar().agregar_inmueble(tipo_inmueble, numero, piso, coeficiente, apartamento_dependiente_id)
        return Response(result)

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated], url_path='agregar-usuario-apartamento')
    def agregar_usuario_apartamento(self, request):
        usuario_id = request.data.get("usuario_id")
        inmueble_id = request.data.get("inmueble_id")
        is_autorizado = request.data.get("is_autorizado", False)
        is_dueño = request.data.get("is_dueño", True)
        coeficiente = request.data.get("coeficiente", 1.0)
        
        result = ServicioAutomatizar().agregar_usuario_apartamento(usuario_id, inmueble_id, is_autorizado, is_dueño, coeficiente)
        return Response(result)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated], url_path='listar-inmuebles-con-detalles')
    def listar_inmuebles_con_detalles(self, request):
        result = ServicioAutomatizar().listar_inmuebles_con_detalles()
        return Response(result)


from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'usuario', UsuarioViewSet, basename='usuario')
router.register(r'prqs', PQRSViewSet, basename='pqrs')
router.register(r'registro', RegistroVisitantesViewSet, basename='registro')
router.register(r'reservas', ReservaServiceViewSet, basename='reservas')
router.register(r'automatizar', ServicioAutomatizarViewSet, basename='automatizar')

urlpatterns = [
    path('', include(router.urls)),
]