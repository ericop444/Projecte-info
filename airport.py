import os
import matplotlib.pyplot as plt

# -------------------------------------------------------
# Classe Airport: guarda el codi ICAO, latitud, longitud
# i si pertany a un país Schengen
# -------------------------------------------------------
class Airport:
    def __init__(self, code, lat, lon):
        self.code = code
        self.lat = lat
        self.lon = lon
        self.isSchengen = False  # Per defecte False, s'actualitza amb SetSchengen


# -------------------------------------------------------
# Retorna True si el codi ICAO pertany a un país Schengen
# Retorna False si el codi és buit o no és Schengen
# -------------------------------------------------------
def IsSchengenAirport(code):
    # Si el codi és buit o té menys de 2 caràcters, retornem False
    if not code or len(code) < 2:
        return False

    schengen_prefixes = [
        'LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH',
        'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS'
    ]

    if code[:2] in schengen_prefixes:
        return True
    return False


# -------------------------------------------------------
# Actualitza l'atribut isSchengen de l'aeroport
# -------------------------------------------------------
def SetSchengen(airport):
    airport.isSchengen = IsSchengenAirport(airport.code)


# -------------------------------------------------------
# Imprimeix per consola les dades de l'aeroport
# -------------------------------------------------------
def PrintAirport(airport):
    print("ICAO Code:", str(airport.code))
    print("Position: Latitude", str(airport.lat))
    print("Position: Longitude", str(airport.lon))
    if airport.isSchengen:
        print("The airport is from a Schengen country")
    else:
        print("The airport is not from a Schengen country")


# -------------------------------------------------------
# Carrega una llista d'aeroports des d'un fitxer de text
# Format: CODE LAT LON (per exemple: BIKF N635906 W0223620)
# Retorna llista buida si el fitxer no existeix
# -------------------------------------------------------
def LoadAirports(filename):
    airport_list = []

    # Comprovem si el fitxer existeix
    if not os.path.exists(filename):
        print("Error: No s'ha trobat el fitxer", filename)
        return airport_list

    with open(filename, "r") as f:
        lines = f.readlines()

    # Saltem la capçalera (primera línia)
    i = 1
    while i < len(lines):
        parts = lines[i].strip().split()

        # Necessitem almenys 3 parts: codi, lat, lon
        if len(parts) < 3:
            i += 1
            continue

        code = parts[0]
        lat_str = parts[1]
        lon_str = parts[2]

        try:
            # Convertim latitud: format N/S + DDMMSS
            lat_dir = lat_str[0]
            lat_deg = float(lat_str[1:3])
            lat_min = float(lat_str[3:5])
            lat_sec = float(lat_str[5:7])
            lat_decimal = lat_deg + (lat_min / 60) + (lat_sec / 3600)
            if lat_dir == 'S':
                lat_decimal = -lat_decimal

            # Convertim longitud: format E/W + DDDMMSS
            lon_dir = lon_str[0]
            lon_deg = float(lon_str[1:4])
            lon_min = float(lon_str[4:6])
            lon_sec = float(lon_str[6:8])
            lon_decimal = lon_deg + (lon_min / 60) + (lon_sec / 3600)
            if lon_dir == 'W':
                lon_decimal = -lon_decimal

            nou_aeroport = Airport(code, lat_decimal, lon_decimal)
            airport_list.append(nou_aeroport)

        except (ValueError, IndexError):
            # Si hi ha un error de format en una línia, la saltem
            print("Avís: línia amb format incorrecte saltada:", lines[i].strip())

        i += 1

    return airport_list


# -------------------------------------------------------
# Guarda en un fitxer els aeroports Schengen de la llista
# Retorna -1 si la llista és buida o no hi ha cap Schengen
# -------------------------------------------------------
def SaveSchengenAirports(airports, filename):
    if not airports:
        return -1

    schengen_count = 0

    with open(filename, "w") as f:
        f.write("CODE LAT LON\n")

        i = 0
        while i < len(airports):
            a = airports[i]

            if a.isSchengen:
                # Convertim latitud decimal a format NDDMMSS
                lat_dir = 'N' if a.lat >= 0 else 'S'
                lat_abs = abs(a.lat)
                lat_deg_int = int(lat_abs)
                lat_min_int = int((lat_abs - lat_deg_int) * 60)
                lat_sec_int = int(round((lat_abs - lat_deg_int - lat_min_int / 60) * 3600))

                # Corregim possibles desbordaments de segons/minuts
                if lat_sec_int == 60:
                    lat_sec_int = 0
                    lat_min_int += 1
                if lat_min_int == 60:
                    lat_min_int = 0
                    lat_deg_int += 1

                lat_str = lat_dir + str(lat_deg_int).zfill(2) + str(lat_min_int).zfill(2) + str(lat_sec_int).zfill(2)

                # Convertim longitud decimal a format EDDDMMSS
                lon_dir = 'E' if a.lon >= 0 else 'W'
                lon_abs = abs(a.lon)
                lon_deg_int = int(lon_abs)
                lon_min_int = int((lon_abs - lon_deg_int) * 60)
                lon_sec_int = int(round((lon_abs - lon_deg_int - lon_min_int / 60) * 3600))

                if lon_sec_int == 60:
                    lon_sec_int = 0
                    lon_min_int += 1
                if lon_min_int == 60:
                    lon_min_int = 0
                    lon_deg_int += 1

                lon_str = lon_dir + str(lon_deg_int).zfill(3) + str(lon_min_int).zfill(2) + str(lon_sec_int).zfill(2)

                f.write(f"{a.code} {lat_str} {lon_str}\n")
                schengen_count += 1

            i += 1

    # Si no s'ha escrit cap aeroport Schengen, retornem error
    if schengen_count == 0:
        return -1
    return 0


# -------------------------------------------------------
# Afegeix un aeroport a la llista si no existeix ja
# Retorna -1 si l'aeroport ja és a la llista
# -------------------------------------------------------
def AddAirport(airports, airport):
    i = 0
    while i < len(airports):
        if airports[i].code == airport.code:
            return -1  # L'aeroport ja existeix
        i += 1

    airports.append(airport)
    return 0


# -------------------------------------------------------
# Elimina de la llista l'aeroport amb el codi indicat
# Retorna -1 si no es troba l'aeroport
# -------------------------------------------------------
def RemoveAirport(airports, code):
    i = 0
    while i < len(airports):
        if airports[i].code == code:
            del airports[i]
            return 0  # Eliminat correctament
        i += 1
    return -1  # No trobat


# -------------------------------------------------------
# Mostra un gràfic de barres apilades amb el nombre
# d'aeroports Schengen i no-Schengen
# -------------------------------------------------------
def PlotAirports(airports):
    schengen_count = 0
    i = 0
    while i < len(airports):
        if airports[i].isSchengen:
            schengen_count += 1
        i += 1

    non_schengen_count = len(airports) - schengen_count

    plt.bar(['Airports'], [schengen_count], label='Schengen', color='blue')
    plt.bar(['Airports'], [non_schengen_count], bottom=[schengen_count], label='No Schengen', color='red')
    plt.ylabel('Count')
    plt.title('Schengen airports')
    plt.legend()
    plt.show()


# -------------------------------------------------------
# Genera un fitxer KML i l'obre a Google Earth
# Mostra els aeroports amb colors diferents: verd=Schengen, vermell=No Schengen
# -------------------------------------------------------
def MapAirports(airports):
    f = open("mapa_aeropuertos.kml", "w")
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    f.write('<Document>\n')

    i = 0
    while i < len(airports):
        a = airports[i]
        # Verd per Schengen, vermell per No Schengen
        color = "ff00ff00" if a.isSchengen else "ff0000ff"
        f.write('<Placemark>\n')
        f.write('  <name>' + a.code + '</name>\n')
        f.write('  <Style><IconStyle><color>' + color + '</color></IconStyle></Style>\n')
        f.write('  <Point>\n')
        f.write('    <coordinates>' + str(a.lon) + ',' + str(a.lat) + ',0</coordinates>\n')
        f.write('  </Point>\n')
        f.write('</Placemark>\n')
        i += 1

    # Tancament del document (fora del bucle)
    f.write('</Document>\n')
    f.write('</kml>\n')
    f.close()

    print("Fitxer KML generat: mapa_aeropuertos.kml")
    try:
        os.startfile("mapa_aeropuertos.kml")
    except Exception:
        print("Obre el fitxer manualment amb Google Earth.")


# -------------------------------------------------------
# Secció de test: s'executa només quan correm airport.py directament
# -------------------------------------------------------
if __name__ == "__main__":
    lista_principal = LoadAirports("Airports.txt")
    if len(lista_principal) == 0:
        print("Error: No s'han pogut carregar aeroports.")
    else:
        i = 0
        while i < len(lista_principal):
            SetSchengen(lista_principal[i])
            i += 1
        print(f"S'han carregat {len(lista_principal)} aeroports.")
        PlotAirports(lista_principal)
        MapAirports(lista_principal)
        SaveSchengenAirports(lista_principal, "Schengen_Airports.txt")