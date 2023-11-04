
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from requests import Response
import requests
import json
from datetime import datetime, timedelta


def index(request):
    return render( request,"primerTemplate.html")
def sesion(request):
    return render( request,"sesion.html")

@csrf_exempt
def dashboard(request):
    if request.method != 'POST':
        return redirect('/residencia/sesion')
    
    token = request.POST.get('token')
    email = request.POST.get('email')
    password = request.POST.get('password')
    idUser= request.POST.get('idUser')

    
    if not token:
        return redirect('/residencia/sesion')
    
    headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}',
    }
        

    response: Response = requests.post(
            'http://localhost:8000/residencia/usuario/obtener-usuario/', 
            data=json.dumps({
            "email": f"{email}",
            "password": f"{password}"
        }),
    headers=headers)
    responseZonaComun: Response = requests.get(
            'http://localhost:8000/residencia/usuario/listar-zona-comun/', 
            headers=headers)
    
    if response.status_code != 200 or responseZonaComun.status_code != 200:
        return redirect('/residencia/sesion')
    zonaComun=responseZonaComun.json()
   
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
    else:
        return redirect('/residencia/sesion')
    
    requestRol: Response = requests.get(
                        'http://localhost:8000/residencia/prqs/listado-pqrsd-admin/',
                        headers=headers)
    prqrs = None
    if requestRol.status_code >= 200 or requestRol.status_code <= 205:
            prqrs =requestRol.json()
            if not prqrs:
                prqrs = [{"id":"",
                "usuario": f"",
                "fecha_registro": "",
                "tipo_pqrs": "",
                "estado": "",
                "mensaje": "",
                "responsable": ""}]
    else:
        return redirect('/residencia/sesion')
    
    reservasEncargados=None
    requestRol: Response = requests.get(
                        'http://localhost:8000/residencia/reservas/listado-para-encargados/',
                        headers=headers)
  
    if requestRol.status_code >= 200 or requestRol.status_code <= 205:
            reservasEncargados =requestRol.json()
            if not prqrs:
                prqrs = [{"Apartamento":"",
                "Responsable": f"",
                "FechaFin": "",
                "FechaInicio": "",
                "estado": "",
                "ReciboPago": "",
                "DepositoEntregado": ""}]
    else:
        return redirect('/residencia/sesion')
    
    
            
    usuario = response.json()     
    context = {"usuario":usuario,"zona_comun":zonaComun,"roles":roles,"prqrs":prqrs ,"reservasEncargados":reservasEncargados}
    for z in context["zona_comun"]:
        z.update({"token":token,"idUsuario":idUser})
    response = render(request, "dashboard.html",context)
    hora_expiracion = datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)
    if datetime.now() >= hora_expiracion:
        hora_expiracion += timedelta(days=1)

    response.set_cookie('token', token, expires=hora_expiracion)
    return response

def reservation(request):
    return render(request,"reservation.html")
