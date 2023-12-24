from bs4 import BeautifulSoup
import urllib.request
import datetime

urlPrimera = 'https://www.resultados-futbol.com/primera2024/grupo1/calendario'

def convertir_fecha(fecha):
    month_map = {"Ene": "Jan", "Feb": "Feb", "Mar": "Mar", "Abr": "Apr", "May": "May", "Jun": "Jun",
                 "Jul": "Jul", "Ago": "Aug", "Sep": "Sep", "Oct": "Oct", "Nov": "Nov", "Dic": "Dec"}

    day, month, year = date_str.split()
    month = month_map[month]

    date = datetime.datetime.strptime(f"{day} {month} {year}", "%d %b %Y")
    return date.strftime("%d/%m/%Y")

def extraer_jugadores(nombre_equipo):
    lista_jugadores = []
    url = 'https://www.resultados-futbol.com/plantilla/' + nombre_equipo.replace(' ', '-')
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f, 'lxml')
    jugadores = s.find_all('tr', itemprop='employee')
    for jugador in jugadores:
        nombre = jugador.find('th', class_='sdata_player_name').find('span').text.strip()
        equipo = nombre_equipo
        edad = jugador.find('td', class_='birthdate').text.strip()
        dorsal = jugador.find('td', class_='num').text.strip()
        posicion = jugador.find_previous('th', class_='axis').text.strip() #this may be wrong
        nacionalidad = jugador.find('td', class_='ori').find('img')['src']
        foto = jugador.find('td', class_='sdata_player_img').find('img')['src']
        lista_jugadores.append([nombre, equipo, edad, dorsal, posicion, nacionalidad, foto])
    return lista_jugadores


def extraer_equipos(partido):
    lista_equipos = []
    nombre_local = partido.find('td', class_='equipo1').find_all('a')[1].text.strip()
    nombre_visitante = partido.find('td', class_='equipo2').find_all('a')[1].text.strip()
    logo_local = partido.find('td', class_='equipo1').find('img')['src']
    logo_visitante = partido.find('td', class_='equipo2').find('img')['src']
    url_local = partido.find('td', class_='equipo1').find_all('a')[1]['href']
    url_visitante = partido.find('td', class_='equipo2').find_all('a')[1]['href']
    lista_equipos.append([nombre_local, logo_local, url_local])
    lista_equipos.append([nombre_visitante, logo_visitante, url_visitante])
    extraer_jugadores(nombre_local)
    extraer_jugadores(nombre_visitante)
    return lista_equipos

def extraer_partidos(url_jornada):
    lista_partidos = []
    f = urllib.request.urlopen(url_jornada)
    s = BeautifulSoup(f, 'lxml')
    partidos_even = s.find_all('tr', class_='vevent')
    partidos_impar = s.find_all('tr', class_='vevent impar')
    for partido in partidos_even:
        equipos = extraer_equipos(partido)
        equipo_local = equipos[0][0]
        equipo_visitante = equipos[1][0]
        goles_local = partido.find('a', class_='url').find('span', class_='clase').text.strip().split('-')[0]
        goles_visitante = partido.find('a', class_='url').find('span', class_='clase').text.strip().split('-')[1]
        fecha = convertir_fecha(partido.find('td', class_='fecha').text.strip())
        lista_partidos.append([equipo_local, equipo_visitante, goles_local, goles_visitante, fecha])
    for partido in partidos_impar:
        equipos = extraer_equipos(partido)
        goles_local = partido.find('td', class_='rstd').a.text.strip()
        goles_visitante = partido.find('td', class_='rstd').a.text.strip()
        fecha = partido.find('td', class_='fecha').text.strip()
        lista_partidos.append([equipo_local, equipo_visitante, goles_local, goles_visitante, fecha])
    return lista_partidos

def extraer_jornadas():
    lista_jornadas = []
    f = urllib.request.urlopen(urlPrimera)
    s = BeautifulSoup(f, 'lxml')
    lista_link_jornadas = s.find_all('div', class_='boxhome boxhome-2col')
    for link_jornadas in lista_link_jornadas:
        url_jornada = 'https://www.resultados-futbol.com/' + link_jornadas.a['href']
        f = urllib.request.urlopen(url_jornada)
        s = BeautifulSoup(f, 'lxml')
        numero_jornada = s.find('div', class_='j_cur').a.text.strip().split(' ')[1]
        lista_partidos = extraer_partidos(url_jornada)
        fechas_even = s.find_all('tr', class_='vevent')
        fecha_impar = s.find_all('tr', class_='vevent impar')
        fecha_inicio = convertir_fecha(fechas_even[0].find('td', class_='fecha').text.strip())
        fecha_fin = convertir_fecha(fecha_impar[-1].find('td', class_='fecha').text.strip())
        lista_jornadas.append([numero_jornada, lista_partidos, fecha_inicio, fecha_fin])
    return lista_jornadas



