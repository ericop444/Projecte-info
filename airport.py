import os
import matplotlib.pyplot as plt

class Airport:
    def __init__(self, code, lat, lon):
        self.code = code
        self.lat = lat
        self.lon = lon
        self.isSchengen = False

def IsSchengenAirport(code):
    schengen = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH',
                'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']
    if code[:2] in schengen:
        return True
    return False

def SetSchengen(airport):
    airport.isSchengen = IsSchengenAirport(airport.code)

def PrintAirport(airport):
    if airport.isSchengen:
        print("The airport is from a Schengen country")
    else:
        print("The airport is not from a Schengen country")
    print("ICAO Code:", str(airport.code))
    print("Position: Latitude", str(airport.lat))
    print("Position: Longitude", str(airport.lon))

def LoadAirports(Airports):
    airport_list = []
    if not os.path.exists(Airports):
        return airport_list
    with open(Airports, "r") as f:
        lines = f.readlines()
        for line in lines[1:]:
            parts = line.split(" ")
            if len(parts) < 3:
                continue
            code = parts[0]
            lat_str = parts[1]
            lon_str = parts[2]

            lat_d = lat_str[0]
            lat_deg = float(lat_str[1:3])
            lat_min = float(lat_str[3:5])
            lat_sec = float(lat_str[5:7])
            lat_decimal = lat_deg + (lat_min / 60) + (lat_sec / 3600)
            if lat_d == 'S':
                lat_decimal = -lat_decimal

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

def SaveSchengenAirports(airports, filename):
    if not airports:
        return -1
    with open(filename, "w") as f:
        f.write("CODE LAT LON\n")
        schengen_count = 0
        for a in airports:
            if a.isSchengen:
                lat_dir = 'N' if a.lat >= 0 else 'S'
                lat_abs = abs(a.lat)
                lat_deg_int = int(lat_abs)
                lat_min_int = int((lat_abs - lat_deg_int) * 60)
                lat_sec_int = int(round((lat_abs - lat_deg_int - lat_min_int / 60) * 3600))

                if lat_sec_int == 60:
                    lat_sec_int = 0
                    lat_min_int += 1
                if lat_min_int == 60:
                    lat_min_int = 0
                    lat_deg_int += 1

                s_lat_deg = str(lat_deg_int).zfill(2)
                s_lat_min = str(lat_min_int).zfill(2)
                s_lat_sec = str(lat_sec_int).zfill(2)
                lat_str = lat_dir + s_lat_deg + s_lat_min + s_lat_sec

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

                s_lon_deg = str(lon_deg_int).zfill(3)
                s_lon_min = str(lon_min_int).zfill(2)
                s_lon_sec = str(lon_sec_int).zfill(2)
                lon_str = lon_dir + s_lon_deg + s_lon_min + s_lon_sec

                f.write(f"{a.code} {lat_str} {lon_str}\n")
                schengen_count += 1
    if schengen_count == 0:
        return -1
    return 0

def AddAirport(airports, airport):
    for a in airports:
        if a.code == airport.code:
            return -1
    airports.append(airport)
    return 0

def RemoveAirport(airports, code):
    for i in range(len(airports)):
        if airports[i].code == code:
            del airports[i]
            return 0
    return -1

def PlotAirports(airports):
    schengen_count = sum(1 for a in airports if a.isSchengen)
    non_schengen_count = len(airports) - schengen_count

    plt.bar(['Airports'], [schengen_count], label='Schengen', color='blue')
    plt.bar(['Airports'], [non_schengen_count], bottom=[schengen_count], label='No Schengen', color='red')
    plt.ylabel('Count')
    plt.title('Schengen airports')
    plt.legend()
    plt.show()

def MapAirports(airports):
    f = open("mapa_aeropuertos.kml", "w")
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    f.write('<Document>\n')

    for a in airports:
        color = "ff00ff00" if a.isSchengen else "ff0000ff"
        f.write('<Placemark>\n')
        f.write('  <name>' + a.code + '</name>\n')
        f.write('  <Style><IconStyle><color>' + color + '</color></IconStyle></Style>\n')
        f.write('  <Point>\n')
        f.write('    <coordinates>' + str(a.lon) + ',' + str(a.lat) + ',0</coordinates>\n')
        f.write('  </Point>\n')
        f.write('</Placemark>\n')

    # ¡ESTO AHORA ESTÁ FUERA DEL BUCLE!
    f.write('</Document>\n')
    f.write('</kml>\n')
    f.close()

    print("Archivo KML generado.")
    try:
        os.startfile("mapa_aeropuertos.kml")
    except Exception:
        print("Guarda el archivo y ábrelo manualmente.")

# ¡ESTO AHORA ESTÁ EN EL MARGEN IZQUIERDO!
if __name__ == "__main__":
    lista_principal = LoadAirports("Airports.txt")
    if len(lista_principal) == 0:
        print("Error: No se han podido cargar aeropuertos.")
    else:
        for aero in lista_principal:
            SetSchengen(aero)
        print(f"Se han cargado {len(lista_principal)} aeropuertos.")
        PlotAirports(lista_principal)
        MapAirports(lista_principal)
        SaveSchengenAirports(lista_principal, "Schengen_Airports.txt")