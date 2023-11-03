
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from requests import Response
import requests
import json

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
            
    usuario = response.json()     
    context = {"usuario":usuario,"zona_comun":zonaComun}
    for z in context["zona_comun"]:
        z.update({"token":token,"idUsuario":idUser})
    response = render(request, "dashboard.html",context)
    response.set_cookie('token', token)
    return response

def reservation(request):
    return render(request,"reservation.html")
