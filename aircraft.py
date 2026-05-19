import os
import math
import matplotlib.pyplot as plt
from airport import IsSchengenAirport, LoadAirports

# -------------------------------------------------------
# Classe Aircraft: representa un vol que arriba a LEBL
# Guarda id, aerolínia, aeroport d'origen i hora d'aterratge
# -------------------------------------------------------
class Aircraft:
    def __init__(self, aircraft_id, airline, origin, time):
        self.id = aircraft_id
        self.airline = airline
        self.origin = origin
        self.time = time  # Format hh:mm


# -------------------------------------------------------
# Carrega una llista de vols des d'un fitxer de text
# Format: AIRCRAFT ORIGIN ARRIVAL AIRLINE
# Retorna llista buida si el fitxer no existeix
# Les línies amb format incorrecte es salten
# -------------------------------------------------------
def LoadArrivals(filename):
    lista_aviones = []

    # Comprovem si el fitxer existeix
    if not os.path.exists(filename):
        print("Error: No s'ha trobat el fitxer", filename)
        return lista_aviones

    with open(filename, "r") as f:
        lineas = f.readlines()

    # Saltem la capçalera (primera línia)
    z = 1
    while z < len(lineas):
        partes = lineas[z].strip().split()

        if len(partes) == 4:
            id_avion = partes[0]
            origen = partes[1]
            hora = partes[2]
            compania = partes[3]

            # Comprovem que l'hora té el format correcte hh:mm
            if ":" in hora and (len(hora) == 4 or len(hora) == 5):
                nuevo_avion = Aircraft(id_avion, compania, origen, hora)
                lista_aviones.append(nuevo_avion)
            else:
                print("Avís: línia amb hora incorrecta saltada:", lineas[z].strip())
        z += 1

    return lista_aviones


# -------------------------------------------------------
# Mostra un histograma amb el nombre d'aterratges per hora
# Retorna si la llista és buida
# -------------------------------------------------------
def PlotArrivals(aircrafts):
    if not aircrafts:
        print("Error: Llista de vols buida")
        return

    hores = []
    i = 0
    while i < len(aircrafts):
        a = aircrafts[i]
        try:
            hora = int(a.time.split(':')[0])
            hores.append(hora)
        except (ValueError, AttributeError):
            print("Avís: error de format a la línia", i + 1)
        i += 1

    plt.hist(hores, bins=range(25), edgecolor='black', align='left')
    plt.title('Aterratges per Hora')
    plt.xlabel('Hora del dia (0 - 23)')
    plt.ylabel('Nombre d\'aterratges')
    plt.xticks(range(24))
    plt.grid(axis='y', alpha=0.75)
    plt.show()


# -------------------------------------------------------
# Guarda la informació dels vols en un fitxer de text
# El format de sortida és el mateix que el d'entrada
# Retorna -1 si la llista és buida
# -------------------------------------------------------
def SaveFlights(aircrafts, filename):
    if not aircrafts:
        print("Error: Llista de vols buida")
        return -1

    try:
        with open(filename, "w") as f:
            f.write("AIRCRAFT ORIGIN ARRIVAL AIRLINE\n")
            i = 0
            while i < len(aircrafts):
                a = aircrafts[i]
                # Si algun camp és buit, posem '-'
                a_id = a.id if a.id else "-"
                a_origin = a.origin if a.origin else "-"
                a_time = a.time if a.time else "-"
                a_airline = a.airline if a.airline else "-"
                f.write(f"{a_id} {a_origin} {a_time} {a_airline}\n")
                i += 1
        return 0

    except Exception as e:
        print(f"Error al guardar el fitxer: {e}")
        return -1


# -------------------------------------------------------
# Mostra un gràfic de barres amb el nombre de vols per aerolínia
# Retorna si la llista és buida
# -------------------------------------------------------
def PlotAirlines(aircrafts):
    if len(aircrafts) == 0:
        print("Error: El vector d'avions és buit.")
        return

    noms_companyies = []
    comptador_vols = []

    z = 0
    while z < len(aircrafts):
        cia = aircrafts[z].airline
        trobada = False

        k = 0
        while k < len(noms_companyies):
            if noms_companyies[k] == cia:
                comptador_vols[k] += 1
                trobada = True
            k += 1

        if not trobada:
            noms_companyies.append(cia)
            comptador_vols.append(1)
        z += 1

    plt.bar(noms_companyies, comptador_vols, color='skyblue')
    plt.xlabel('Companyia Aèria')
    plt.ylabel('Nombre de Vols')
    plt.title('Vols per Companyia (Arribades a LEBL)')
    plt.show()


# -------------------------------------------------------
# Mostra un gràfic de barres apilades: vols Schengen vs No-Schengen
# Retorna si la llista és buida
# -------------------------------------------------------
def PlotFlightsType(aircrafts):
    if len(aircrafts) == 0:
        print("Error: La llista d'avions és buida")
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
    ax.set_ylabel('Nombre de vols')
    ax.set_title('Arribades Schengen vs No-Schengen')
    ax.legend()
    plt.show()


# -------------------------------------------------------
# Genera un fitxer KML amb les trajectòries dels vols
# Línies blaves = Schengen, línies vermelles = No-Schengen
# -------------------------------------------------------
def MapFlights(aircrafts):
    if len(aircrafts) == 0:
        print("Error: La llista d'avions és buida.")
        return

    # Carreguem la llista d'aeroports per trobar les coordenades d'origen
    airports_list = LoadAirports("Airports.txt")
    if not airports_list:
        print("Error: No s'han pogut carregar els aeroports")
        return

    # Coordenades de LEBL (Barcelona El Prat)
    lebl_lat = 41.297445
    lebl_lon = 2.0832941

    f = open("flights_map.kml", "w")
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    f.write('<Document>\n')
    # Estil per als vols Schengen (blau) i No-Schengen (vermell)
    f.write('  <Style id="schengenStyle"><LineStyle><color>ffff0000</color><width>2</width></LineStyle></Style>\n')
    f.write('  <Style id="nonSchengenStyle"><LineStyle><color>ff0000ff</color><width>2</width></LineStyle></Style>\n')

    i = 0
    while i < len(aircrafts):
        ac = aircrafts[i]
        origin_lat = 0.0
        origin_lon = 0.0
        found = False

        # Busquem l'aeroport d'origen a la llista
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
            f.write('    <name>Ruta ' + ac.origin + ' - LEBL (' + ac.airline + ')</name>\n')
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
    print("Fitxer KML generat: flights_map.kml")
    try:
        import os
        os.startfile("flights_map.kml")
    except Exception:
        print("Obre el fitxer manualment amb Google Earth.")


# -------------------------------------------------------
# Retorna la llista de vols que provenen de més de 2000 km
# Utilitza la fórmula de Haversine per calcular la distància
# -------------------------------------------------------
def LongDistanceArrivals(aircrafts):
    result = []

    # Coordenades de LEBL
    bcn_lat = 41.2974
    bcn_lon = 2.0833

    # Carreguem aeroports per obtenir coordenades d'origen
    airports = LoadAirports("Airports.txt")

    i = 0
    while i < len(aircrafts):
        origin_code = aircrafts[i].origin

        # Busquem l'aeroport d'origen
        j = 0
        while j < len(airports):
            if airports[j].code == origin_code:
                R = 6371  # Radi de la Terra en km

                # Convertim a radians
                lat1 = math.radians(bcn_lat)
                lon1 = math.radians(bcn_lon)
                lat2 = math.radians(airports[j].lat)
                lon2 = math.radians(airports[j].lon)

                # Fórmula de Haversine
                dlat = abs(lat1 - lat2)
                dlon = abs(lon1 - lon2)
                a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                dist = R * c

                if dist > 2000:
                    result.append(aircrafts[i])
                break
            j += 1
        i += 1

    return result


# -------------------------------------------------------
# Secció de test: s'executa només quan correm aircraft.py directament
# -------------------------------------------------------
if __name__ == "__main__":
    vuelos = LoadArrivals("Arrivals.txt")
    if vuelos:
        print(f"Carregats {len(vuelos)} vols.")
        PlotArrivals(vuelos)
        PlotAirlines(vuelos)
        PlotFlightsType(vuelos)
        MapFlights(vuelos)
        llarga_distancia = LongDistanceArrivals(vuelos)
        print(f"Vols de llarga distància (>2000km): {len(llarga_distancia)}")
        MapFlights(llarga_distancia)
        SaveFlights(vuelos, "Arrivals_output.txt")