class Aircraft:
    def __init__(self, aircraft_id, airline, origin, time):

        self.id = aircraft_id
        self.airline = airline
        self.origin = origin
        self.time = time

import os

#Funcio 1
def LoadArrivals(filename):
    lista_aviones = []

    # Comprobamos si el archivo existe
    if not os.path.exists(filename):
        return lista_aviones

    # Abrimos y leemos las líneas
    with open(filename, "r") as f:
        lineas = f.readlines()

    # while
    # Empezamos en z = 1 para saltarnos la cabecera
    z = 1
    while z < len(lineas):
        linea_actual = lineas[z]

        #  línea por espacios
        partes = linea_actual.split()

        # VALIDACIÓN 1: El enunciado dice que debe tener 4 partes
        if len(partes) == 4:
            id_avion = partes[0]
            origen = partes[1]
            hora = partes[2]
            compania = partes[3]

            # que la hora tenga el formato correcto (hh:mm)
            # Miramos si tiene los ":" y si mide 4 o 5 caracteres (ej: "0:04" o "12:30")
            if ":" in hora and (len(hora) == 4 or len(hora) == 5):
                # Creamos eobjeto con los datos
                # (Recuerda el orden de tu __init__: id, compania, origen, hora)
                nuevo_avion = Aircraft(id_avion, compania, origen, hora)

                # Lo añadimos al vector
                lista_aviones.append(nuevo_avion)

        # Pasamos a la siguiente línea
        z = z + 1

    return lista_aviones


import matplotlib.pyplot as plt

#Funcio 2
def PlotArrivals (aircrafts):
    if not aircrafts:
        print("Error: Lista de vuelos vacia")
        return

    hora_at =[]
    i =0
    while i < len(aircrafts):
        a = aircrafts[i]
        #separem hora dels minuts i afegim al vector hora_at
        try:
            hora = int(a.time.split(':')[0])
            hora_at.append(hora)
        except (ValueError, AttributeError):
            print("Linea",i+1," con errores de formato")
        i +=1
    #creem grafic 24 barres
    plt.hist(hora_at, bins=range(25), edgecolor='black', align='left')
    #configurem grafic
    plt.title('Aterrizajes por Hora')
    plt.xlabel('Hora del día (0 - 23)')
    plt.ylabel('Número de aterrizajes')
    plt.xticks(range(24))
    plt.grid(axis='y', alpha=0.75)

    plt.show()

#Funcio 3
def SaveFlights(aircrafts, filename):
    if not aircrafts:
        print("Error: Lista de vuelos vacia")
        return
    try:
        with open(filename, "w") as f:
            f.write("AIRCRAFT ORIGIN ARRIVAL AIRLINE\n")

            i = 0
            while i < len(aircrafts):
                a = aircrafts[i]
                a_id = a.id if a.id else "-"
                a_origin = a.origin if a.origin else "-"
                a_time = a.time if a.time else "-"
                a_airline = a.airline if a.airline else "-"

                f.write(f"{a_id} {a_origin} {a_time} {a_airline}\n")
                i += 1

        return 0
    #retornem error si n'hi ha
    except Exception as e:
        print(f"Ha ocurrido un error al guardar el archivo: {e}")
        return -1

# funcion 4:
def PlotAirlines(aircrafts):
    # lista está vacía?
    if len(aircrafts) == 0:
        print("Error: El vector de aviones está vacío. No se puede generar el gráfico.")
        return

    nombres_companias = []
    conteo_vuelos = []

    z = 0
    while z < len(aircrafts):
        avion = aircrafts[z]
        cia = avion.airline

        encontrada = False
        k = 0
        while k < len(nombres_companias):
            if nombres_companias[k] == cia:
                conteo_vuelos[k] = conteo_vuelos[k] + 1
                encontrada = True
            k = k + 1

        if encontrada == False:
            nombres_companias.append(cia)
            conteo_vuelos.append(1)

        z = z + 1

    plt.bar(nombres_companias, conteo_vuelos, color='skyblue')
    plt.xlabel('Compañía Aérea')
    plt.ylabel('Número de Vuelos')
    plt.title('Vuelos por Compañía (Llegadas a LEBL)')
    plt.show()

# Función 5
from airport import IsSchengenAirport  # Necesitamos importar esta función también

def PlotFlightsType(aircrafts):
    # Recibe una lista de vuelos y muestra en una gráfica los schengen y los no schengen
    # Si la lista está vacia se muestra un error en la pantalla:

    if len(aircrafts) == 0:
        print("Error: Aircraft list is empty, therefore cannot generate plot")
        return  # Salimos de la function para que no muestre nada más

    schengen_count = 0
    non_schengen_count = 0

    i = 0
    while i < len(aircrafts):
        if IsSchengenAirport(aircrafts[i].origin):
            schengen_count += 1
        else:
            non_schengen_count += 1
        i += 1

    # Creamos el gráfico con forma "stacked bars"
    labels = ['Arrivals']  # Solo necesitamos esta columna, ya que las dos salidas van encima.

    fig, ax = plt.subplots()

    ax.bar(labels, [schengen_count], label='Schengen', color='blue')

    # Para que se apilen las gráficas el parámetro 'bottom' empieza donde acaba la otra:
    ax.bar(labels, [non_schengen_count], bottom=[schengen_count], label='No Schengen', color='lightcoral')

    ax.set_ylabel('Number of flights')
    ax.set_title('Schengen vs Non-Schengen Arrivals')
    ax.legend()  # Esto muestra la leyenda de colores

    plt.show()

# Función 6
from airport import LoadAirports

def MapFlights(aircrafts):
    # Muestra en Google Earth la trayectoria de todos los vuelos de la lista, desde su origen hasta LEBL.
    if len(aircrafts) == 0:
        print("Error: The list of aircrafts is empty. Map cannot be generated.")
        return

    airports_list = LoadAirports("Airports.txt")
    if not airports_list:
        print("Error: No se han podido cargar los aeropuertos")
        return
    # Coordenadas de Barcelona LEBL
    lebl_lat = 41.297445
    lebl_lon = 2.0832941

    f = open("flights_map.kml", "w")

    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    f.write('<Document>\n')

    # Estilos KML (Azul para Schengen, Rojo para no Schengen)
    f.write('  <Style id="schengenStyle">\n')
    f.write('    <LineStyle>\n')
    f.write('      <color>ffff0000</color>\n')
    f.write('      <width>2</width>\n')
    f.write('    </LineStyle>\n')
    f.write('  </Style>\n')
    f.write('  <Style id="nonSchengenStyle">\n')
    f.write('    <LineStyle>\n')
    f.write('      <color>ff0000ff</color>\n')
    f.write('      <width>2</width>\n')
    f.write('    </LineStyle>\n')
    f.write('  </Style>\n')

    i = 0

    while i < len(aircrafts):
        ac = aircrafts[i]

        origin_lat = 0.0
        origin_lon = 0.0
        found = False

        # Buscamos las coordenadas del aeropuerto con la lista cargada
        j = 0
        while j < len(airports_list) and not found:

            if airports_list[j].code == ac.origin:
                origin_lat = airports_list[j].coordinates[0]
                origin_lon = airports_list[j].coordinates[1]
                found = True
            j = j+1

        # Dibujamos la ruta si encontramos el aeropuerto de origen
        if found:
            if IsSchengenAirport(ac.origin):
                style = "#schengenStyle"
            else:
                style = "#nonSchengenStyle"

            f.write('  <Placemark>\n')
            f.write('    <name>Route ' + ac.origin + ' - LEBL (' + ac.airline + ')</name>\n')
            f.write('    <styleUrl>' + style + '</styleUrl>\n')
            f.write('    <LineString>\n')
            f.write('      <altitudeMode>clampToGround</altitudeMode>\n')
            f.write('      <extrude>1</extrude>\n')
            f.write('      <tessellate>1</tessellate>\n')
            f.write('      <coordinates>\n')

            f.write('        ' + str(origin_lon) + ',' + str(origin_lat) + '\n')
            f.write('        ' + str(lebl_lon) + ',' + str(lebl_lat) + '\n')
            f.write('      </coordinates>\n')
            f.write('    </LineString>\n')
            f.write('  </Placemark>\n')

        i = i+1

    f.write('</Document>\n')
    f.write('</kml>\n')
    f.close()

    print("El mapa se ha guardado correctamente como 'flights_map.kml'")
import os
import math


# ===== CLASSE AIRPORT =====
class Airport:
    def __init__(self, code, lat, lon):
        self.code = code
        self.lat = lat
        self.lon = lon

def LoadAirports(Airports):
    airport_list = []

    if not os.path.exists(Airports):
        return airport_list

    with open(Airports, "r") as f:
        lines = f.readlines()

        for line in lines[1:]:

            parts = line.split()
            if len(parts) < 3:
                continue

            code = parts[0]
            lat_str = parts[1]
            lon_str = parts[2]

            # LAT
            lat_d = lat_str[0]
            lat_deg = float(lat_str[1:3])
            lat_min = float(lat_str[3:5])
            lat_sec = float(lat_str[5:7])

            lat_decimal = lat_deg + (lat_min / 60) + (lat_sec / 3600)
            if lat_d == 'S':
                lat_decimal = -lat_decimal

            # LON
            lon_d = lon_str[0]
            lon_deg = float(lon_str[1:4])
            lon_min = float(lon_str[4:6])
            lon_sec = float(lon_str[6:8])

            lon_decimal = lon_deg + (lon_min / 60) + (lon_sec / 3600)
            if lon_d == 'W':
                lon_decimal = -lon_decimal

            nuevo_aeropuerto = Airport(code, lat_decimal, lon_decimal)
            airport_list.append(nuevo_aeropuerto)

    return airport_list


# ===== HAVERSINE =====
def haversine(lat1, lon1, lat2, lon2):
    R = 6371

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c

def LongDistanceArrivals(aircrafts):

    result = []

    airports = LoadAirports("airports.txt")  # carregues aeroports

    # Barcelona
    bcn_lat = 41.2974
    bcn_lon = 2.0833

    for aircraft in aircrafts:

        origin_code = aircraft.origin

        # buscar aeroport
        for airport in airports:
            if airport.code == origin_code:

                dist = haversine(bcn_lat, bcn_lon, airport.lat, airport.lon)

                if dist > 2000:
                    result.append(aircraft)

                break

    return result


# ===== TEST =====
if __name__ == "__main__":
    aircrafts = LoadArrivals("arrivals.txt")

    # prova la funció nova
    long_flights = LongDistanceArrivals(aircrafts)

    print("Vols de més de 2000 km:", len(long_flights))