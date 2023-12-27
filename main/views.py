from django.shortcuts import render
from main.models import Equipo


def index(request):
    return render(request, 'home.html')

def listado_equipos(request):
    equipos = Equipo.objects.all()
    return render(request, 'listado-equipos.html', {'equipos': equipos})