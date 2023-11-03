from django.urls import path
from residencia import views

urlpatterns = [
    path("a/", views.index),
    path("sesion/", views.sesion),
    path("reservation/", views.reservation),
    path("dashboard/", views.dashboard),
]