import os
import math
import matplotlib.pyplot as plt
from airport import IsSchengenAirport, LoadAirports

class Aircraft:
    def __init__(self, aircraft_id, airline, origin, time):
        self.id = aircraft_id
        self.airline = airline
        self.origin = origin
        self.time = time

def LoadArrivals(filename):
    lista_aviones = []
    if not os.path.exists(filename):
        return lista_aviones

    with open(filename, "r") as f:
        lineas = f.readlines()

    z = 1
    while z < len(lineas):
        linea_actual = lineas[z]
        partes = linea_actual.split()

        if len(partes) == 4:
            id_avion = partes[0]
            origen = partes[1]
            hora = partes[2]
            compania = partes[3]

            if ":" in hora and (len(hora) == 4 or len(hora) == 5):
                nuevo_avion = Aircraft(id_avion, compania, origen, hora)
                lista_aviones.append(nuevo_avion)
        z += 1
    return lista_aviones

def PlotArrivals(aircrafts):
    if not aircrafts:
        print("Error: Lista de vuelos vacia")
        return
    hora_at = []
    i = 0
    while i < len(aircrafts):
        a = aircrafts[i]
        try:
            hora = int(a.time.split(':')[0])
            hora_at.append(hora)
        except (ValueError, AttributeError):
            print("Linea", i + 1, " con errores de formato")
        i += 1

    plt.hist(hora_at, bins=range(25), edgecolor='black', align='left')
    plt.title('Aterrizajes por Hora')
    plt.xlabel('Hora del día (0 - 23)')
    plt.ylabel('Número de aterrizajes')
    plt.xticks(range(24))
    plt.grid(axis='y', alpha=0.75)
    plt.show()

def SaveFlights(aircrafts, filename):
    if not aircrafts:
        print("Error: Lista de vuelos vacia")
        return -1
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
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")
        return -1

def PlotAirlines(aircrafts):
    if len(aircrafts) == 0:
        print("Error: El vector de aviones está vacío.")
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
                conteo_vuelos[k] += 1
                encontrada = True
            k += 1
        if not encontrada:
            nombres_companias.append(cia)
            conteo_vuelos.append(1)
        z += 1

    plt.bar(nombres_companias, conteo_vuelos, color='skyblue')
    plt.xlabel('Compañía Aérea')
    plt.ylabel('Número de Vuelos')
    plt.title('Vuelos por Compañía (Llegadas a LEBL)')
    plt.show()

def PlotFlightsType(aircrafts):
    if len(aircrafts) == 0:
        print("Error: Aircraft list is empty")
        return

    schengen_count = 0
    non_schengen_count = 0

    i = 0
    while i < len(aircrafts):
        if IsSchengenAirport(aircrafts[i].origin):
            schengen_count += 1
        else:
            non_schengen_count += 1
        i += 1

    labels = ['Arrivals']
    fig, ax = plt.subplots()
    ax.bar(labels, [schengen_count], label='Schengen', color='blue')
    ax.bar(labels, [non_schengen_count], bottom=[schengen_count], label='No Schengen', color='lightcoral')
    ax.set_ylabel('Number of flights')
    ax.set_title('Schengen vs Non-Schengen Arrivals')
    ax.legend()
    plt.show()

def MapFlights(aircrafts):
    if len(aircrafts) == 0:
        print("Error: The list of aircrafts is empty.")
        return

    airports_list = LoadAirports("Airports.txt")
    if not airports_list:
        print("Error: No se han podido cargar los aeropuertos")
        return

    lebl_lat = 41.297445
    lebl_lon = 2.0832941

    f = open("flights_map.kml", "w")
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    f.write('<Document>\n')
    f.write('  <Style id="schengenStyle"><LineStyle><color>ffff0000</color><width>2</width></LineStyle></Style>\n')
    f.write('  <Style id="nonSchengenStyle"><LineStyle><color>ff0000ff</color><width>2</width></LineStyle></Style>\n')

    i = 0
    while i < len(aircrafts):
        ac = aircrafts[i]
        origin_lat = 0.0
        origin_lon = 0.0
        found = False

        j = 0
        while j < len(airports_list) and not found:
            if airports_list[j].code == ac.origin:
                origin_lat = airports_list[j].lat
                origin_lon = airports_list[j].lon
                found = True
            j += 1

        if found:
            style = "#schengenStyle" if IsSchengenAirport(ac.origin) else "#nonSchengenStyle"
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
        i += 1

    f.write('</Document>\n')
    f.write('</kml>\n')
    f.close()
    print("Mapa KML generado.")

def LongDistanceArrivals(aircrafts):
    result = []
    airports = LoadAirports("Airports.txt")
    bcn_lat = 41.2974
    bcn_lon = 2.0833

    for aircraft in aircrafts:
        origin_code = aircraft.origin
        for ap in airports:
            if ap.code == origin_code:
                R = 6371
                lat1 = math.radians(bcn_lat)
                lon1 = math.radians(bcn_lon)
                lat2 = math.radians(ap.lat)
                lon2 = math.radians(ap.lon)

                dlat = abs(lat1 - lat2)
                dlon = abs(lon1 - lon2)

                a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

                dist = R * c
                if dist > 2000:
                    result.append(aircraft)
                break
    return result

if __name__ == "__main__":
    vuelos = LoadArrivals("Arrivals.txt")
    if vuelos:
        print(f"Cargados {len(vuelos)} vuelos.")

class Gate:
    def __init__(self, name): #li poso un nom
        self.name = name #guardo un nom
        self.occupied = False #comprovo si esta ocupada
        self.aircraft_id = None #quin avió hi ha

