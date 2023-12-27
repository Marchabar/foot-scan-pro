from django.shortcuts import render
from main.models import Equipo, Jornada, Partido


def index(request):
    return render(request, 'home.html')

def listado_equipos(request):
    equipos = Equipo.objects.all()
    return render(request, 'listado-equipos.html', {'equipos': equipos})

def listado_jornadas(request):
    jornadas = Jornada.objects.all()
    return render(request, 'listado-jornadas.html', {'jornadas': jornadas})

def listado_partidos_jornada(request, id_jornada):
    jornada = Jornada.objects.get(id_jornada=id_jornada)
    partidos = Partido.objects.filter(jornada=jornada)
    return render(request, 'listado-partidos-jornadas.html', {'jornada':jornada,'partidos': partidos})