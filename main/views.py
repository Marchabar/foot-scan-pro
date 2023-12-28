from django.shortcuts import render
from main.models import Equipo, Jornada, Partido, Jugador
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.query import Or



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

def listado_jugadores(request):
    query = request.GET.get('query', '')

    if query:
        directorio = 'Index'  
        ix = open_dir(directorio)

        with ix.searcher() as searcher:
            nombre_query = QueryParser("nombre", ix.schema).parse(query)
            edad_query = QueryParser("edad", ix.schema).parse(query)
            posicion_query = QueryParser("posicion", ix.schema).parse(query)
            nacionalidad_query = QueryParser("nacionalidad_nombre", ix.schema).parse(query)
            equipo_query = QueryParser("equipo", ix.schema).parse(query)

            combined_query = Or([nombre_query, edad_query, posicion_query, nacionalidad_query, equipo_query])

            jugadores = searcher.search(combined_query, limit=None)

            jugador_objects = [Jugador.objects.get(pk=int(jugador['id_jugador'])) for jugador in jugadores]
    else:
        jugador_objects = Jugador.objects.all()

    return render(request, 'listado-jugadores.html', {'jugadores': jugador_objects, 'query': query})