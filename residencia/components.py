

from reactpy import component, html,use_state,event,web
from reactpy_django.components import django_css,django_js
from datetime import datetime
from requests import Response
import requests
import json
import pytz

@component
def hello_world(recipient: str):
    return html.h1(f"Hello {recipient}!")
 


@component
def sesion():
    email, setEmail = use_state('')
    password, setPassword = use_state('')
    message, setMessage = use_state('')
    show_more, set_show_more = use_state(False)
    user_id , setUser = use_state('')
    access , setAcces = use_state('')
    paso,setPaso =use_state(False)
    
    def handleEmailChange(new_email):
        setEmail(new_email["target"]["value"])

    def handlePasswordChange(new_password):
        setPassword(new_password["target"]["value"])

    def handleLogin(event):
        headers = {
            'Content-Type': 'application/json',
        }
        

        response: Response = requests.post(
            'http://localhost:8000/residencia/usuario/iniciar/', 
            data=json.dumps({
            "email": f"{email}",
            "password": f"{password}"
        }),
        headers=headers)
       
        if response.status_code == 200:
            usuario = response.json()
            
            setAcces(usuario["access"])
            setUser(usuario["usuario"])
            setPaso(True)
        else:
            print("No paso!!")
            set_show_more(not show_more)
            setMessage(response.json()["message"])
            
    
    return html.form({"class":"form form-login","action":"/residencia/dashboard/" ,"method":"post"},
                     html.fieldset(
        html.legend("Ingresa el email y contraseña."),
        html.div({ "class":"input-block"},
                 html.label({ "for":"email"},"Email:"),
                 html.input({"type":"email","id":"email","onChange":handleEmailChange})
                ),
        html.div({ "class":"input-block"},
                html.label({ "for":"password"},"Password:"),
                 html.input({"type":"password","id":"password","onChange":handlePasswordChange,"required":True}))
        ,(html.p({"style":{ "color": "red",          
                                    "font-size": "12px",   
                                    "margin-top": "5px",     
                                    "font-weight": "bold"}},message) if show_more else "")
        ,html.input({"type":"hidden","name":"token","value":f"{access}"})
        ,html.input({"type":"hidden","name":"email","value":f"{email}"})
        ,html.input({"type":"hidden","name":"password","value":f"{password}"})
        ,html.input({"type":"hidden","name":"idUser","value":f"{user_id}"})
    ),(
        html.button({ "class":"btn-login","type" :"submit","onClick":event(handleLogin)},"Continuar") if paso else html.button({ "class":"btn-login","type" :"submit","onClick":event(handleLogin,prevent_default=True)},"Iniciar")),
                     django_css("css/sesion.css"),django_js("script/sesion.js")
                      )

@component
def crear_reserva(recipient, recipientUsuario):
    now =  datetime.now()
    formatted_date = now.strftime("%b %d, %Y")
    formatted_date_html = now.strftime("%Y-%m-%d")
    zone, setZone = use_state('')
    departureTime, setdepartureTime = use_state(None)
    returnTime, setreturnTime = use_state(None)
    message,setMessage = use_state('')
    show_more,setShowMore= use_state(False)
    cedulas , setCedula =use_state({})
    count , setCount = use_state(0)
    countZone, setCountZone = use_state(0)
    error, setError = use_state(0)
    nombreRol, setNombreRol= use_state("")
    idrol , setidRol = use_state("")
    cedulaPersonal , setCedulaPersonal = use_state("")
    
    token = recipient[0]["token"]
    headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}',
    }
    roles = None
    requestRol: Response = requests.post(
                    'http://localhost:8000/residencia/usuario/listar_roles/',
                    headers=headers)
    if requestRol.status_code >= 200 or requestRol.status_code <= 205:
        roles =requestRol.json()
        if not roles:
            roles = ["Agrega un nuevo rol"]
    

    def handleSelectZone(id_zone):
        setShowMore(False)
        setCountZone(id_zone["target"]["value"])
        setZone(id_zone["target"]["value"])
        
  
    
    def handledepartureTime(datatime):
        setShowMore(False)
        setdepartureTime(pytz.timezone('America/Bogota').localize(datetime.strptime(datatime["target"]["value"],"%Y-%m-%dT%H:%M")).astimezone(pytz.utc))
    
    def handlereturnTime(datatime):
        setShowMore(False)
        setreturnTime(pytz.timezone('America/Bogota').localize(datetime.strptime(datatime["target"]["value"],"%Y-%m-%dT%H:%M")).astimezone(pytz.utc))
        
    def handleIdUsuario(_):
        print("No se puede modificar el id del usuario")
    
    def handleCedula(cedula):  
        setShowMore(False)     
        cedulas[str(cedula["selection"]["anchorOffset"])] =cedula["target"]["value"]
      
    def handleMore(counts): 
        setCount(count+1)
        
    def handleReservation(reservation):
        pass_test = True
        if not zone:
            pass_test= False
            setShowMore(True)
            setMessage("Elije una Zona común")
        if not departureTime:
            pass_test= False
            setShowMore(True)
            setMessage("Elije una Hora de salida")
        if not returnTime:
            pass_test= False
            setShowMore(True)
            setMessage("Elije una Hora de entrada")
        if len(cedulas)<1:
            pass_test= False
            setShowMore(True)
            setMessage("Debe de haber mas de un invitado")
        if pass_test:
            token = recipient[0]["token"]
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}',
            }
            responseZonaComun: Response = requests.post(
                    'http://localhost:8000/residencia/reservas/realizar-reserva/',
                    data= json.dumps({
                    "usuario_id" : recipient[0]["idUsuario"],
                    "zona_comun_id" : zone,
                    "hora_entrada" : returnTime.isoformat(),
                    "hora_salida" : departureTime.isoformat(),
                    "invitados" :json.dumps(list(cedulas.values()))
                    }),
                
                    headers=headers)
        
        
            if responseZonaComun.status_code != 200 and responseZonaComun.status_code != 204:
                setShowMore(True)
                setMessage(responseZonaComun.json()["message"])
    
    def nada(a):
        pass
    
    def handleNombreRol(target):
        setShowMore(False)
        setNombreRol(target["target"]["value"])
    
    def handleAgregarRol(_):
        pass_test = True
        if not nombreRol:
            pass_test= False
            setShowMore(True)
            setMessage("Elije un nombre para el nuevo rol")
        
        if pass_test:
            token = recipient[0]["token"]
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}',
            }
            responseZonaComun: Response = requests.post(
                    'http://localhost:8000/residencia/usuario/agregar-rol/',
                    data= json.dumps({
                    "nombre" : nombreRol,
                    }),
                    headers=headers)
        
        
            if responseZonaComun.status_code != 200 and responseZonaComun.status_code != 204:
                setShowMore(True)
                setMessage(responseZonaComun.json()["message"])
            
    def handleSelectRol(request):
        setShowMore(False)
        setidRol(request["target"]["value"])
        
    def handleCedulaPersonal(target):
        setShowMore(False)
        setCedulaPersonal(target["target"]["value"])
            
    def handleUsuarioRol(request):
        pass_test = True
        if not cedulaPersonal:
            pass_test = False
            setShowMore(True)
            setMessage("Ingrese cedula de la persona")
        if not idrol:
            pass_test = False
            setShowMore(True)
            setMessage("Seleccione o vuelva a seleccionar el rol")

        if pass_test:
            token = recipient[0]["token"]
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}',
            }
            responseZonaComun: Response = requests.post(
                    'http://localhost:8000/residencia/usuario/agregar-rol-al-usuario/',
                    data= json.dumps({
                    "id" : idrol,
                    "cedula":cedulaPersonal
                    }),
                    headers=headers)
            if responseZonaComun.status_code != 200 and responseZonaComun.status_code != 204:
                setShowMore(True)
                setMessage(responseZonaComun.json()["message"])
        
        
        
    
    
    propiedadesUsuario = html.ul({ "class":"project-list"},
                html.li({"class":"project-item"},
                    html.div({"class":"card2 project-card"},
                        html.h3({"class":"card-title"},"Reservación de Zona Común"),
                        html.time({"class":"card-date" ,"datetime":f"{formatted_date_html}"},f"{formatted_date}"),
                        html.div({"class":"form-group"},
                            html.label({"for":"zone"},"Zona común:"),
                            html.select({"id":"zone", "class":"custom-select","onChange":handleSelectZone},
                                html.option({"value":"","class":"custom-select","onBlur":nada},"Selecciona una opcion"),
                                [html.option({"value":f"{recipient[i]['id']}","class":"custom-select","onBlur":nada},recipient[i]["nombre"]) for i in range(len(recipient))],
                            )
                        ),  html.div({"class":"form-group"},
                                html.label({"for":"username"},"Nombre de usuario:"),
                                html.input({"type":"text", "id":"username", "class":"custom-input", "placeholder":"Escribe tu nombre","onBlur":handleIdUsuario})
                        ),  html.div({"class":"form-group"},
                                html.label({"for":"departureTime"},"Hora de salida:"),
                                html.input({"type":"datetime-local", "id":"departureTime", "class":"custom-input","onBlur":handledepartureTime})
                        ),  html.div({"class":"form-group"},
                                html.label({"for":"returnTime"},"Hora de entrada:"),
                                html.input({"type":"datetime-local", "id":"returnTime", "class":"custom-input","onBlur":handlereturnTime})
                        ),  html.div({"class":"form-group cedula-group"},
                                    html.label({"for":"cedula"},"Invitados por cedula:"),
                                    html.div({"id":"cedula-list"},
                                        [html.input({ "type":"text", "class":"custom-input cedula-input" ,"placeholder":"Escribe la cédula","onBlur":handleCedula}) for _ in range(count+1)],
                                    ),
                                    html.div({"class":"cedula-buttons"},
                                            html.button({"id":"addCedula", "class":"custom-button","onClick":event(handleMore,prevent_default=True)},"Agregar Cédula"),
                                            html.button({ "id":"removeCedula" ,"class":"custom-button"},"Quitar Cédula"),
                                    )
                          
                        ), html.button({"id":"eviaButton","class":"custom-button reserve-button","onClick":event(handleReservation,prevent_default=True)},"Reservar")
                        ,(html.p({"style":{ "color": "red",          
                                    "font-size": "12px",   
                                    "margin-top": "5px",     
                                    "font-weight": "bold"},"class":"reserve-button"},message) if show_more else ""),
                    ),
                    
                ),html.li({"class":"project-item zone-item"},
                    html.div({"class":"card project-card zone-card"},
                        html.time({"class":"card-date", "datetime":"2022-04-09"}, "Apr 09, 2022"),
                        html.div({"class":"zone-wrapper"},
                            html.h3({"class":"zone-title"}, f"{[r['nombre'] for r in recipient if str(countZone) == str(r['id'])][0]  if len([r['nombre'] for r in recipient if str(countZone) == str(r['id'])]) > 0 else 'Elije una opcion' }"),
                            html.div({"class":"zone-details"},
                                html.div({"class":"detail-item"},
                                    html.span({"class":"detail-label"}, "Precio:"),
                                    html.span({"class":"detail-value"}, f"${[r['precio'] for r in recipient if str(countZone) == str(r['id'])][0]  if len([r['nombre'] for r in recipient if str(countZone) == str(r['id'])]) > 0 else '' }")
                                ),
                                html.div({"class":"detail-item"},
                                    html.span({"class":"detail-label"}, "Depósito:"),
                                    html.span({"class":"detail-value"}, f"{['Sí' if r['esDeposito'] else 'No' for r in recipient if str(countZone) == str(r['id'])][0]  if len([r['nombre'] for r in recipient if str(countZone) == str(r['id'])]) > 0 else ''}")
                                ),
                                html.div({"class":"detail-item"},
                                    html.span({"class":"detail-label"}, "Disponible:"),
                                    html.span({"class":"detail-value"},  f"{['Sí' if r['esDisponible'] else 'No' for r in recipient if str(countZone) == str(r['id'])][0]  if len([r['nombre'] for r in recipient if str(countZone) == str(r['id'])]) > 0 else ''}")
                                ),
                                html.div({"class":"detail-item"},
                                    html.span({"class":"detail-label"}, "Máx. Personas:"),
                                    html.span({"class":"detail-value"}, f"{[r['maxPersonas'] for r in recipient if str(countZone) == str(r['id'])][0]  if len([r['nombre'] for r in recipient if str(countZone) == str(r['id'])]) > 0 else ''}")
                                ),
                                html.div({"class":"detail-item"},
                                    html.span({"class":"detail-label"}, "Máx. Horas:"),
                                    html.span({"class":"detail-value"}, f"{[r['maxHora'] for r in recipient if str(countZone) == str(r['id'])][0]  if len([r['nombre'] for r in recipient if str(countZone) == str(r['id'])]) > 0 else ''}")
                                )
                            ),
                           
                        )
                    )
                ),django_css("css/dashboard.css"),django_js("script/dashboard.js")  
    )
    
    propiedadesAdmin = html.ul({ "class":"project-list"},
                html.li({"class":"project-item"},
                    html.div({"class":"card2 project-card"},
                        html.h4({"class":"card-title"},"Configuracion admin"),
                        html.time({"class":"card-date" ,"datetime":f"{formatted_date_html}"},f"{formatted_date}"),
                        html.div({"class":"form-section"},
                                html.h4("Agregar Zona Comun"),
                                html.div({"class":"form-row"},
                                        html.label({"for":"nombre"},"Nombre:"),
                                        html.input({"type":"text","id":"nombre","placeholder":"Nombre de la zona"})
                                ),html.div({"class":"form-row"},
                                        html.label({"for":"maxHora"},"Máx. Horas:"),
                                        html.input({"type":"number","id":"maxHora","placeholder":"Máximas horas"})
                                ),html.div({"class":"form-row"},
                                        html.label({"for":"esPrecio"},"Precio:"),
                                        html.div({"class":"checkbox-container"},
                                                html.input({"type":"checkbox","id":"esPrecio","placeholder":"Precio"}),

                                        )
                                        
                                ),html.div({"class":"form-row"},
                                        html.label({"for":"esDeposito"},"Depósito:"),
                                        html.div({"class":"checkbox-container"},
                                            html.input({"type":"checkbox","id":"esDeposito","placeholder":"Máximas horas"})
                                        )
                                ),html.div({"class":"form-row"},
                                        html.label({"for":"maxPersona"},"Máx. Personas:"),
                                        html.input({"type":"number","id":"maxPersona","placeholder":"Máximas personas"})
                                ),html.div({"class":"form-row"},
                                        html.label({"for":"precio"},"Precio:"),
                                        html.input({"type":"text","id":"precio","placeholder":"Precio"})
                                ),html.div({"class":"form-row"},
                                        html.button({"type":"button","class":"add-zone-button"},"Agregar Zona"),
                                )
                        ),html.div({"class":"form-section"},
                                html.h4("Agregar usuario al inmueble"),
                                html.div({"class":"form-row"},
                                        html.label({"for":"tipo_inmueble"},"Tipo de Inmueble:"),
                                        html.select({"id":"tipo_inmueble"},
                                            html.option({"value":"Apartamento"},"Apartamento"),
                                            html.option({"value":"Parqueadero"},"Parqueadero"),
                                            html.option({"value":"CuartoÚtil"},"CuartoÚtil"),
                                        )
                                ),html.div({"class":"form-row"},
                                        html.label({"for":"numero"},"Número:"),
                                        html.input({"type":"text","id":"numero","placeholder":"Número"})
                                ),html.div({"class":"form-row"},
                                        html.label({"for":"coeficiente"},"Coeficiente:"),
                                        html.input({"type":"text","id":"coeficiente","placeholder":"Coeficiente"})
                                ),html.div({"class":"form-row"},
                                        html.label({"for":"piso"},"Piso:"),
                                        html.input({"type":"text","id":"piso","placeholder":"Piso"})
                                ),html.div({"class":"form-row"},
                                        html.label({"for":"apartamento_dependiente_id"},"ID Apartamento Dependiente:"),
                                        html.input({"type":"text","id":"apartamento_dependiente_id","placeholder":"Codigo inmueble"})
                                ),html.div({"class":"form-row invisible"},
                                        html.label({"for":"a"},"hidden"),
                                        html.input({"type":"text","id":"a","placeholder":"Hidden"})
                                ),html.div({"class":"form-row"},
                                        html.button({"type":"button","class":"add-zone-button"},"Agregar Inmueble"),
                                )
                        
                        ),html.div({"class":"form-section"},
                                html.h4("Agregar usuario al apartamento"),
                                html.div({"class":"form-row"},
                                        html.label({"for":"cedula"},"Cedula:"),
                                        html.input({"type":"text","id":"cedula","placeholder":"Cedula:"})
                                ),html.div({"class":"form-row"},
                                        html.label({"for":"inmueble"},"Codigo inmueble:"),
                                        html.input({"type":"text","id":"inmueble","placeholder":"Codigo inmueble"})
                                ),html.div({"class":"form-row"},
                                        html.label({"for":"coeficiente"},"Coeficiente:"),
                                        html.input({"type":"text","id":"coeficiente","placeholder":"Número"})
                                ),html.div({"class":"form-row"},
                                        html.label({"for":"esAutorizado"},"¿Esta autorizado?:"),
                                        html.div({"class":"checkbox-container"},
                                                html.input({"type":"checkbox","id":"esAutorizado","placeholder":"¿Esta autorizado?"}),

                                        )      
                                ),html.div({"class":"form-row"},
                                        html.label({"for":"esDueño"},"¿Es dueño del apartamento?:"),
                                        html.div({"class":"checkbox-container"},
                                                html.input({"type":"checkbox","id":"esDueño","placeholder":"Es dueño del apartamento?"}),

                                        )      
                                ),html.div({"class":"form-row"},
                                        html.button({"type":"button","class":"add-zone-button"},"Agregar Inmueble"),
                                )
                        ),html.div({"class":"form-section"},
                                html.h4("Sobre el rol"),
                                html.div({"class":"form-row"},
                                        html.label({"for":"cedula"},"Cedula del usuario:"),
                                        html.input({"type":"text","id":"cedula","placeholder":"Cedula:","onChange":handleCedulaPersonal})
                                ),html.div({"class":"form-row"},
                                        html.label({"for":"tipo_rol"},"Rol al asignar:"),
                                        html.select({"id":"tipo_rol","onChange":handleSelectRol},
                                            [html.option({"value":f"{roles[i]['id']}"},roles[i]["nombre"]) for i in range(len(roles))],
                                            
                                        )
                                ),html.div({"class":"form-row"},
                                        html.button({"type":"button","class":"add-zone-button","onClick":event(handleUsuarioRol,prevent_default=True)},"Asignar rol a la persona"),
                                ),html.div({"class":"form-row"},
                                        html.label({"for":"rol"},"Nombre del rol:"),
                                        html.input({"type":"text","id":"rol","placeholder":"Ingresa nombre del rol","onChange":handleNombreRol})
                                ),html.div({"class":"form-row"},
                                        html.button({"type":"button","class":"add-zone-button","onClick":event(handleAgregarRol,prevent_default=True)},"Agregar Rol"),
                                )
                        ),(html.p({"style":{ "color": "red",          
                                    "font-size": "12px",   
                                    "margin-top": "5px",     
                                    "font-weight": "bold"},"class":"reserve-button centered"},message) if show_more else "")
                    ),
                    
                ),html.li({"class":"project-item zone-item"},
                    html.div({"class":"card project-card zone-card"},
                        html.time({"class":"card-date" ,"datetime":f"{formatted_date_html}"},f"{formatted_date}"),
                    )
                ) ,django_css("css/dashboard.css"),django_js("script/dashboard.js")  
    )
    return propiedadesAdmin if recipientUsuario["rol"].lower() == "administrador" else propiedadesUsuario
    
                    
      

#Button({})

            

              


              

              
    

