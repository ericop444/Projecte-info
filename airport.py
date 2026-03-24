class Airport:
    def __init__(self, code, lat, lon):
        self.code = code
        self.lat = lat
        self.lon = lon
        self.isSchengen = False



def IsSchengenAirport (code):
    schengen = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH',
                'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']
    if code[:2] in schengen: #nomes mirem les dues primeres lletres del code
        return True
    return False

def SetSchengen (airport):
    airport.isSchengen = IsSchengenAirport(airport.code)

def PrintAirport (airport):
    if airport.isSchengen:
        print("The airport is from a Schengen country")
    else:
        print("The airport is not from a Schengen country")
    print("ICAO Code:", str(airport.code))
    print("Position: Latitude", str(airport.lat))
    print("Position: Longitude", str(airport.lon))

import os
def LoadAirports (Airports):
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
            lat_str = (parts[1])
            lon_str = (parts[2])

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

    with open(filename, "w") as f:      #f=open(filename,w)
        f.write("CODE LAT LON\n")

        schengen_count = 0
        for a in airports: #que haga el proceso para todos los aeropuertos (a pase por todos)
            if a.isSchengen:
                lat_dir = 'N' if a.lat >= 0 else 'S'
                lat_abs = abs(a.lat)
                lat_deg = int(lat_abs)
                lat_min = int((lat_abs - lat_deg) * 60)
                lat_sec = int(round((lat_abs - lat_deg - lat_min / 60) * 3600))

                if lat_sec == 60:
                    lat_sec = 0
                    lat_min += 1
                if lat_min == 60:
                    lat_min = 0
                    lat_deg += 1
                lat_str = f"{lat_dir}{lat_deg:02d}{lat_min:02d}{lat_sec:02d}"

                lon_dir = 'E' if a.lon >= 0 else 'W'
                lon_abs = abs(a.lon)
                lon_deg = int(lon_abs)
                lon_min = int((lon_abs - lon_deg) * 60)
                lon_sec = int(round((lon_abs - lon_deg - lon_min / 60) * 3600))

                if lon_sec == 60:
                    lon_sec = 0
                    lon_min += 1
                if lon_min == 60:
                    lon_min = 0
                    lon_deg += 1
                lon_str = f"{lon_dir}{lon_deg:03d}{lon_min:02d}{lon_sec:02d}"


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