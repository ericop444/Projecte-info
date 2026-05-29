import os
import math
import matplotlib.pyplot as plt
from airport import IsSchengenAirport, LoadAirports

# -------------------------------------------------------
# Classe Aircraft: representa un vol que arriba/surt de LEBL
# Guarda id, aerolínia, aeroport d'origen, hora d'aterratge,
# aeroport de destinació i hora de sortida (v4)
# -------------------------------------------------------
class Aircraft:
    def __init__(self, aircraft_id, airline, origin, time,
                 destination=None, departure_time=None):
        self.id             = aircraft_id
        self.airline        = airline
        self.origin         = origin
        self.time           = time          # hora d'arribada hh:mm (o None)
        self.destination    = destination   # codi ICAO destinació (v4)
        self.departure_time = departure_time  # hora de sortida hh:mm (v4)


# -------------------------------------------------------
# Carrega una llista de vols (arribades) des d'un fitxer
# Format: AIRCRAFT ORIGIN ARRIVAL AIRLINE
# Retorna llista buida si el fitxer no existeix
# -------------------------------------------------------
def LoadArrivals(filename):
    lista_aviones = []

    if not os.path.exists(filename):
        print("Error: No s'ha trobat el fitxer", filename)
        return lista_aviones

    with open(filename, "r") as f:
        lineas = f.readlines()

    z = 1
    while z < len(lineas):
        partes = lineas[z].strip().split()

        if len(partes) == 4:
            id_avion  = partes[0]
            origen    = partes[1]
            hora      = partes[2]
            compania  = partes[3]

            if ":" in hora and (len(hora) == 4 or len(hora) == 5):
                nuevo_avion = Aircraft(id_avion, compania, origen, hora)
                lista_aviones.append(nuevo_avion)
            else:
                print("Avís: línia amb hora incorrecta saltada:", lineas[z].strip())
        z += 1

    return lista_aviones


# -------------------------------------------------------
# Carrega una llista de sortides des d'un fitxer (v4)
# Format: AIRCRAFT DESTINATION DEPARTURE AIRLINE
# Retorna llista buida i codi -1 si el fitxer no existeix
# -------------------------------------------------------
def LoadDepartures(filename):
    lista_sortides = []

    if not os.path.exists(filename):
        print("Error: No s'ha trobat el fitxer", filename)
        return lista_sortides, -1

    with open(filename, "r") as f:
        lineas = f.readlines()

    z = 1
    while z < len(lineas):
        partes = lineas[z].strip().split()

        if len(partes) == 4:
            id_avion    = partes[0]
            desti       = partes[1]
            hora_sort   = partes[2]
            compania    = partes[3]

            if ":" in hora_sort and (len(hora_sort) == 4 or len(hora_sort) == 5):
                # Creem un Aircraft amb camps d'arribada buits
                avion = Aircraft(id_avion, compania, None, None,
                                 destination=desti, departure_time=hora_sort)
                lista_sortides.append(avion)
            else:
                print("Avís: línia amb hora incorrecta saltada:", lineas[z].strip())
        z += 1

    return lista_sortides


# -------------------------------------------------------
# Combina la llista d'arribades i sortides (v4)
# Fusiona els Aircraft amb el mateix id i horaris compatibles
# (hora d'arribada anterior a la de sortida)
# Un avió pot aterrar i sortir més d'una vegada al dia.
# Retorna codi -1 si alguna de les llistes és buida
# -------------------------------------------------------
def MergeMovements(arrivals, departures):
    if not arrivals or not departures:
        print("Error: alguna de les llistes és buida")
        return [], -1

    # Comencem amb una còpia de les arribades (objectes nous)
    lista_moviments = []
    i = 0
    while i < len(arrivals):
        a = arrivals[i]
        merged.append(Aircraft(a.id, a.airline, a.origin, a.time,
                               a.destination, a.departure_time))
        i += 1

    # Afegim les sortides: si existeix una arribada amb el mateix id i
    # hora d'arribada < hora de sortida → fusionem; si no, afegim nou
    d = 0
    while d < len(departures):
        dep = departures[d]
        trobat = False

        m = 0
        while m < len(lista_moviments) and not trobat:
            ac = lista_moviments[m]
            # Comprovem que l'id coincideix i els horaris son compatibles
            if ac.id == dep.id and ac.departure_time is None:
                # Comprovem compatibilitat horària
                horari_ok = False
                if ac.time is not None and dep.departure_time is not None:
                    try:
                        arr_h, arr_m = map(int, ac.time.split(':'))
                        dep_h, dep_m = map(int, dep.departure_time.split(':'))
                        arr_total = arr_h * 60 + arr_m
                        dep_total = dep_h * 60 + dep_m
                        if arr_total < dep_total:
                            horari_ok = True
                    except ValueError:
                        pass

                if horari_ok:
                    ac.destination    = dep.destination
                    ac.departure_time = dep.departure_time
                    trobat = True
            m += 1

        if not trobat:
            # Afegim la sortida com a nou element (avió que ve de la nit
            # o segon vol del dia)
            lista_moviments.append(Aircraft(dep.id, dep.airline, None, None,
                                   dep.destination, dep.departure_time))
        d += 1

    return lista_moviments


# -------------------------------------------------------
# Retorna una llista amb els avions nocturns (v4):
# avions que NOMES tenen sortida (sense dades d'arribada)
# Retorna codi -1 si la llista és buida
# -------------------------------------------------------
def NightAircraft(aircrafts):
    if not aircrafts:
        print("Error: la llista d'avions és buida")
        return [], -1

    nocturs = []
    i = 0
    while i < len(aircrafts):
        ac = aircrafts[i]
        # Avió nocturn: sense origen ni hora d'arribada
        if ac.origin is None and ac.time is None and ac.departure_time is not None:
            nocturs.append(ac)
        i += 1

    return nocturs


# -------------------------------------------------------
# Mostra un histograma amb el nombre d'aterratges per hora
# -------------------------------------------------------
def PlotArrivals(aircrafts):
    if not aircrafts:
        print("Error: Llista de vols buida")
        return

    hores = []
    i = 0
    while i < len(aircrafts):
        a = aircrafts[i]
        if a.time is not None:
            try:
                hora = int(a.time.split(':')[0])
                hores.append(hora)
            except (ValueError, AttributeError):
                print("Avís: error de format a la línia", i + 1)
        i += 1

    plt.hist(hores, bins=range(25), edgecolor='black', align='left')
    plt.title('Aterratges per Hora')
    plt.xlabel('Hora del dia (0 - 23)')
    plt.ylabel("Nombre d'aterratges")
    plt.xticks(range(24))
    plt.grid(axis='y', alpha=0.75)
    plt.show()


# -------------------------------------------------------
# Guarda la informació dels vols en un fitxer de text
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
                a_id      = a.id      if a.id      else "-"
                a_origin  = a.origin  if a.origin  else "-"
                a_time    = a.time    if a.time     else "-"
                a_airline = a.airline if a.airline  else "-"
                f.write(f"{a_id} {a_origin} {a_time} {a_airline}\n")
                i += 1
        return 0
    except Exception as e:
        print(f"Error al guardar el fitxer: {e}")
        return -1


# -------------------------------------------------------
# Mostra un gràfic de barres amb el nombre de vols per aerolínia
# -------------------------------------------------------
def PlotAirlines(aircrafts):
    if len(aircrafts) == 0:
        print("Error: El vector d'avions és buit.")
        return

    noms_companyies = []
    comptador_vols  = []

    z = 0
    while z < len(aircrafts):
        cia     = aircrafts[z].airline
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
# Mostra un gràfic de barres apilades: Schengen vs No-Schengen
# -------------------------------------------------------
def PlotFlightsType(aircrafts):
    if len(aircrafts) == 0:
        print("Error: La llista d'avions és buida")
        return

    schengen_count     = 0
    non_schengen_count = 0

    i = 0
    while i < len(aircrafts):
        if aircrafts[i].origin and IsSchengenAirport(aircrafts[i].origin):
            schengen_count += 1
        else:
            non_schengen_count += 1
        i += 1

    labels = ['Arrivals']
    fig, ax = plt.subplots()
    ax.bar(labels, [schengen_count],     label='Schengen',    color='blue')
    ax.bar(labels, [non_schengen_count], bottom=[schengen_count],
           label='No Schengen', color='lightcoral')
    ax.set_ylabel('Nombre de vols')
    ax.set_title('Arribades Schengen vs No-Schengen')
    ax.legend()
    plt.show()


# -------------------------------------------------------
# Genera un fitxer KML amb les trajectòries dels vols
# -------------------------------------------------------
def MapFlights(aircrafts):
    if len(aircrafts) == 0:
        print("Error: La llista d'avions és buida.")
        return

    airports_list = LoadAirports("Airports.txt")
    if not airports_list:
        print("Error: No s'han pogut carregar els aeroports")
        return

    lebl_lat = 41.297445
    lebl_lon = 2.0832941

    f = open("flights_map.kml", "w")
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    f.write('<Document>\n')
    f.write('  <Style id="schengenStyle"><LineStyle><color>ffff0000</color>'
            '<width>2</width></LineStyle></Style>\n')
    f.write('  <Style id="nonSchengenStyle"><LineStyle><color>ff0000ff</color>'
            '<width>2</width></LineStyle></Style>\n')

    i = 0
    while i < len(aircrafts):
        ac = aircrafts[i]
        if ac.origin is None:
            i += 1
            continue

        origin_lat = 0.0
        origin_lon = 0.0
        found      = False

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
            f.write('        ' + str(lebl_lon)   + ',' + str(lebl_lat)   + '\n')
            f.write('      </coordinates>\n')
            f.write('    </LineString>\n')
            f.write('  </Placemark>\n')
        i += 1

    f.write('</Document>\n')
    f.write('</kml>\n')
    f.close()
    print("Fitxer KML generat: flights_map.kml")
    try:
        os.startfile("flights_map.kml")
    except Exception:
        print("Obre el fitxer manualment amb Google Earth.")


# -------------------------------------------------------
# Retorna la llista de vols que provenen de més de 2000 km
# -------------------------------------------------------
def LongDistanceArrivals(aircrafts):
    llista_llarga = []
    bcn_lat  = 41.2974
    bcn_lon  = 2.0833
    airports = LoadAirports("Airports.txt")

    i = 0
    while i < len(aircrafts):
        origin_code = aircrafts[i].origin
        if origin_code is None:
            i += 1
            continue

        j = 0
        while j < len(airports):
            if airports[j].code == origin_code:
                R    = 6371
                lat1 = math.radians(bcn_lat)
                lon1 = math.radians(bcn_lon)
                lat2 = math.radians(airports[j].lat)
                lon2 = math.radians(airports[j].lon)

                dlat = abs(lat1 - lat2)
                dlon = abs(lon1 - lon2)
                a    = (math.sin(dlat / 2) ** 2 +
                        math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2)
                c    = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                dist = R * c

                if dist > 2000:
                    llista_llarga.append(aircrafts[i])
                break
            j += 1
        i += 1

    return llista_llarga


# -------------------------------------------------------
# Secció de test
# -------------------------------------------------------
if __name__ == "__main__":
    # Test 1: Carreguem arribades
    print("=== Test LoadArrivals ===")
    vuelos = LoadArrivals("Arrivals.txt")
    if vuelos:
        print(f"Carregats {len(vuelos)} vols.")
        PlotArrivals(vuelos)
        PlotAirlines(vuelos)
        PlotFlightsType(vuelos)
        MapFlights(vuelos)

        llarga_distancia = LongDistanceArrivals(vuelos)
        print(f"Vols de llarga distància (>2000km): {len(llarga_distancia)}")

        SaveFlights(vuelos, "Arrivals_output.txt")
    else:
        print("No s'han pogut carregar vols.")

    # Test 2: Carreguem sortides (v4)
    print("\n=== Test LoadDepartures ===")
    sortides = LoadDepartures("Departures.txt")
    if sortides:
        print(f"Carregades {len(sortides)} sortides.")
    else:
        print("No s'han pogut carregar sortides (o fitxer inexistent).")

    # Test 3: MergeMovements (v4)
    if vuelos and sortides:
        print("\n=== Test MergeMovements ===")
        lista_moviments = MergeMovements(vuelos, sortides)
        if isinstance(lista_moviments, list):
            print(f"Total moviments fusionats: {len(lista_moviments)}")
            amb_sortida = sum(1 for ac in lista_moviments if ac.departure_time is not None)
            print(f"  Amb sortida: {amb_sortida}")
            print(f"  Sense sortida: {len(lista_moviments) - amb_sortida}")

    # Test 4: NightAircraft (v4)
    if vuelos and sortides:
        print("\n=== Test NightAircraft ===")
        merged2 = MergeMovements(vuelos, sortides)
        if isinstance(merged2, list):
            nocturs = NightAircraft(merged2)
            if isinstance(nocturs, list):
                print(f"Avions nocturns: {len(nocturs)}")