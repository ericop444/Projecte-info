class Aircraft:
    def __init__(self, aircraft_id, airline, origin, time):

        self.id = aircraft_id
        self.airline = airline
        self.origin = origin
        self.time = time


def LoadArrivals(filename):
    lista_aviones = []

    # Comprobamos si el archivo existe
    if not os.path.exists(filename):
        return lista_aviones

    # Abrimos y leemos las líneas
    f = open(filename, "r")
    lineas = f.readlines()
    f.close()

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
            print("Linea",[i]+1," con errores de formato")
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
