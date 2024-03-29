from bs4 import BeautifulSoup
import urllib.request
import datetime
from unidecode import unidecode
from main.models import Jugador, Equipo, Partido, Jornada
from django.shortcuts import render, redirect
import os
import shutil
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in




urlPrimera = 'https://www.resultados-futbol.com/primera2024/grupo1/calendario'

def convertir_fecha(fecha):
    month_map = {"Ene": "01", "Feb": "02", "Mar": "03", "Abr": "04", "May": "05", "Jun": "06",
                 "Jul": "07", "Ago": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dic": "12"}

    fecha = fecha.split('\n')[0]  
    day, month, year = fecha.split()
    month = month_map[month]

    date = datetime.datetime.strptime(f"{day} {month} {year}", "%d %m %y")
    return date.strftime("%Y-%m-%d")

country_codes =  {
    'es': 'España',
    'mk': 'Macedonia',
    'fr': 'France',
    'gh': 'Ghana',
    'ro': 'Romania',
    'al': 'Albania',
    'uy': 'Uruguay',
    'ar': 'Argentina',
    'sn': 'Senegal',
    'cv': 'Cabo Verde',
    'co': 'Colombia',
    'pt': 'Portugal',
    'mx': 'Mexico',
    'gw': 'Guinea Bissau',
    'br': 'Brasil',
    'be': 'Belgica',
    'ml': 'Mali',
    'rs': 'Serbia',
    'ma': 'Marruecos',
    'ch': 'Suiza',
    'hr': 'Croacia',
    'do': 'Republica Dominicana',
    'ge': 'Georgia',
    'tr': 'Turquia',
    'gp': 'Guadalupe',
    'ua': 'Ucrania',
    've': 'Venezuela',
    'ss': 'Escocia',
    'ru': 'Rusia',
    'no': 'Noruega',
    'jp': 'Japon',
    'ng': 'Nigeria',
    'nl': 'Holanda',
    'gq': 'Guinea Ecuatorial',
    'cd': 'Republica Democratica del Congo',
    'sk': 'Eslovaquia',
    'ca': 'Canada',
    'xk': 'Kosovo',
    'gb': 'Gran Bretaña',
    'de': 'Alemania',
    'us': 'Estados Unidos',
    'pe': 'Peru',
    'ci': 'Costa de Marfil',
    'gr': 'Grecia',
    'il': 'Israel',
    'py': 'Paraguay',
    'cl': 'Chile',
    'tg': 'Togo',
    'ie': 'Irlanda',
    'hn': 'Honduras',
    'hu': 'Hungria',
    'dk': 'Dinamarca',
    'pl': 'Polonia',
    'cm': 'Camerun',
    'at': 'Austria',
    'dz': 'Argelia',
    'it': 'Italia',
    'se': 'Suecia',
}
jugadores_por_equipo = {}
def extraer_jugadores(url_plantilla, nombre_equipo):
    if nombre_equipo in jugadores_por_equipo:
        return jugadores_por_equipo[nombre_equipo]

    lista_jugadores = []
    nombre_equipo = unidecode(nombre_equipo.replace(' ', '-'))
    f = urllib.request.urlopen(url_plantilla)
    s = BeautifulSoup(f, 'lxml')
    jugadores = s.find_all('tr', itemprop='employee')
    for jugador in jugadores:
        nombre = jugador.find('th', class_='sdata_player_name').find('span').text.strip()
        equipo = nombre_equipo
        edad = jugador.find('td', class_='birthdate').text.strip()
        dorsal = jugador.find('td', class_='num').text.strip()
        posicion = jugador.find_previous('th', class_='axis').text.strip() #this may be wrong
        nacionalidad_nombre = country_codes.get(jugador.find('td', class_='ori').find('img')['alt'], 'Unknown')
        foto = jugador.find('td', class_='sdata_player_img').find('img')['src']
        lista_jugadores.append([nombre, equipo, edad, dorsal, posicion, nacionalidad_nombre, foto])
    jugadores_por_equipo[nombre_equipo] = lista_jugadores
    return lista_jugadores
     
equipos_extracted = {}
def extraer_equipos(partido):
    nombre_local = partido.find('td', class_='equipo1').find_all('a')[1].text.strip()
    nombre_visitante = partido.find('td', class_='equipo2').find_all('a')[1].text.strip()
    if nombre_local not in equipos_extracted:
        logo_local = partido.find('td', class_='equipo1').find('img')['src']
        url_local = partido.find('td', class_='equipo1').find_all('a')[1]['href']
        equipos_extracted[nombre_local] = [nombre_local, logo_local, url_local]
        url_plantilla = "https://www.resultados-futbol.com" + url_local
        f = urllib.request.urlopen(url_plantilla)
        s = BeautifulSoup(f, 'lxml')
        url_plantilla = s.find('b', text='Plantilla').parent['href']
        extraer_jugadores(url_plantilla, nombre_local)
        
    if nombre_visitante not in equipos_extracted:
        logo_visitante = partido.find('td', class_='equipo2').find('img')['src']
        url_visitante = partido.find('td', class_='equipo2').find_all('a')[1]['href']
        equipos_extracted[nombre_visitante] = [nombre_visitante, logo_visitante, url_visitante]
        url_plantilla = "https://www.resultados-futbol.com" + url_visitante
        f = urllib.request.urlopen(url_plantilla)
        s = BeautifulSoup(f, 'lxml')
        url_plantilla = s.find('b', text='Plantilla').parent['href']
        extraer_jugadores(url_plantilla, nombre_visitante)
    return equipos_extracted

def extraer_partidos(url_jornada):
    lista_partidos = []
    f = urllib.request.urlopen(url_jornada)
    s = BeautifulSoup(f, 'lxml')
    partidos_even = s.find_all('tr', class_='vevent')
    partidos_impar = s.find_all('tr', class_='vevent impar')
    for partido in partidos_even:
        extraer_equipos(partido)
        equipo_local = partido.find('td', class_='equipo1').find_all('a')[1].text.strip()
        equipo_visitante = partido.find('td', class_='equipo2').find_all('a')[1].text.strip()
        equipo_local = unidecode(equipo_local.replace(' ', '-'))
        equipo_visitante = unidecode(equipo_visitante.replace(' ', '-'))
        result_element = partido.find('span', class_='clase')
        if result_element is not None:
            result_or_time = result_element.text.strip()
        else:
            time_element = partido.find('div', class_='chk_hour')
            if time_element is not None:
                result_or_time = time_element.text.strip()
            else:
                result_or_time = 'x'  
        if '-' in result_or_time:
            goles_local, goles_visitante = result_or_time.split('-')
        else:
            goles_local = goles_visitante = 'x'
        fecha = convertir_fecha(partido.find('td', class_='fecha').text.strip())
        lista_partidos.append([equipo_local, equipo_visitante, goles_local, goles_visitante, fecha])
    for partido in partidos_impar:
        extraer_equipos(partido)
        equipo_local = partido.find('td', class_='equipo1').find_all('a')[1].text.strip()
        equipo_visitante = partido.find('td', class_='equipo2').find_all('a')[1].text.strip()
        equipo_local = unidecode(equipo_local.replace(' ', '-'))
        equipo_visitante = unidecode(equipo_visitante.replace(' ', '-'))
        result_element = partido.find('span', class_='clase')
        if result_element is not None:
            result_or_time = result_element.text.strip()
        else:
            time_element = partido.find('div', class_='chk_hour')
            if time_element is not None:
                result_or_time = time_element.text.strip()
            else:
                result_or_time = 'x'  
        if '-' in result_or_time:
            goles_local, goles_visitante = result_or_time.split('-')
        else:
            goles_local = goles_visitante = 'x'
        fecha = convertir_fecha(partido.find('td', class_='fecha').text.strip())
        lista_partidos.append([equipo_local, equipo_visitante, goles_local, goles_visitante, fecha])
    return lista_partidos

def extraer_jornadas():
    lista_jornadas = []
    f = urllib.request.urlopen(urlPrimera)
    s = BeautifulSoup(f, 'lxml')
    lista_link_jornadas = s.find_all('div', class_='boxhome boxhome-2col')
    numero_jornada = 1
    for link_jornadas in lista_link_jornadas:
        url_jornada = 'https://www.resultados-futbol.com/' + link_jornadas.a['href']
        f = urllib.request.urlopen(url_jornada)
        s = BeautifulSoup(f, 'lxml')
        fechas_even = s.find_all('tr', class_='vevent')
        fecha_impar = s.find_all('tr', class_='vevent impar')
        fecha_inicio = convertir_fecha(fechas_even[0].find('td', class_='fecha').text.strip())
        fecha_fin = convertir_fecha(fecha_impar[-1].find('td', class_='fecha').text.strip())
        lista_partidos = extraer_partidos(url_jornada)
        lista_jornadas.append([numero_jornada, lista_partidos, fecha_inicio, fecha_fin])
        numero_jornada += 1
        
    return lista_jornadas

def populate():
    num_jugadores = 0  
    num_equipos = 0
    num_partidos = 0
    num_jornadas = 0

    Jugador.objects.all().delete()
    Equipo.objects.all().delete()
    Partido.objects.all().delete()
    Jornada.objects.all().delete()

    lista_jornadas = extraer_jornadas()


    equipos = equipos_extracted.values()
    for equipo in equipos:
        num_equipos += 1
        equipo_nombre = unidecode(equipo[0].replace(' ', '-'))
        equipo = Equipo.objects.create(nombre=equipo_nombre, logo=equipo[1], url=equipo[2])
        jugadores = jugadores_por_equipo[equipo_nombre]
        for jugador in jugadores:
            num_jugadores += 1
            jugador = Jugador.objects.create(nombre=jugador[0], equipo=equipo, edad=jugador[2], dorsal=jugador[3], posicion=jugador[4], nacionalidad_nombre=jugador[5], foto=jugador[6])

    for jornada_data in lista_jornadas:
        num_jornadas += 1
        jornada = Jornada.objects.create(numero=jornada_data[0], fecha_inicio=jornada_data[2], fecha_fin=jornada_data[3])
        for partido_data in jornada_data[1]:
            equipo_local, created = Equipo.objects.get_or_create(nombre=partido_data[0])
            equipo_visitante, created = Equipo.objects.get_or_create(nombre=partido_data[1])
            partido, created = Partido.objects.get_or_create(
            equipo_local=equipo_local, 
            equipo_visitante=equipo_visitante, 
            jornada=jornada,
            defaults={
                'goles_local': partido_data[2], 
                'goles_visitante': partido_data[3], 
                'fecha': partido_data[4]
            }
            )
            if created:
                    num_partidos += 1
        
    return ((num_jugadores, num_equipos, num_partidos, num_jornadas))

def populate_whoosh():
    schema_jugadores = Schema(id_jugador=ID(stored=True), nombre=TEXT(stored=True), equipo=TEXT(stored=True), edad=TEXT(stored=True), dorsal=TEXT(stored=True), posicion=TEXT(stored=True), nacionalidad_nombre=TEXT(stored=True))

    if os.path.exists("Index"):
        shutil.rmtree("Index")
    os.mkdir("Index")

    ix_jugadores = create_in("Index", schema_jugadores)
    writer_jugadores = ix_jugadores.writer()
    lista_jugadores = Jugador.objects.all()
    for jugador in lista_jugadores:
        writer_jugadores.update_document(id_jugador=str(jugador.id_jugador), nombre=jugador.nombre, equipo=jugador.equipo.nombre, edad=str(jugador.edad), dorsal=jugador.dorsal, posicion=jugador.posicion, nacionalidad_nombre=jugador.nacionalidad_nombre)
    writer_jugadores.commit()
    return len(lista_jugadores)
    
def cargar(request):
    if request.method == 'POST':
        num_jugadores, num_equipos, num_partidos, num_jornadas = populate()
        num_jugadores_whoosh = populate_whoosh()
        return render(request, 'cargar.html', {'num_jugadores': num_jugadores, 'num_equipos': num_equipos, 'num_partidos': num_partidos, 'num_jornadas': num_jornadas, 'num_jugadores_whoosh': num_jugadores_whoosh})
    
    return render(request, 'confirmacion-cargar.html')



