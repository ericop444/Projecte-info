class Aircraft:
    def __init__(self, aircraft_id, airline, origin, time):

        self.id = aircraft_id
        self.airline = airline
        self.origin = origin
        self.time = time
# función uno
def LoadArrivals(filename):
    lista_aviones = []
    if not os.path.exists(filename): # por si no existe
        return lista_aviones

    f = open(filename, "r")
    lineas = f.readlines() #creamos vector con las lineas
    f.close()

    z = 1 #empezzamos por la 1 q la cero es el titulo
    while z < len(lineas):
        linea_actual = lineas[z]

    # separamos la línea por espacios
    partes = linea_actual.split()

    # VALIDACIÓN 1: debe tener 4 partes
    if len(partes) == 4:
        id_avion = partes[0]
        origen = partes[1]
        hora = partes[2]
        compania = partes[3]

        # VALIDACIÓN 2: formato correcto (hh:mm)
        # Miramos si tiene los ":" y si mide 4 o 5
        if ":" in hora and (len(hora) == 4 or len(hora) == 5):
            # Creamos el objeto con los datos
            # (Recuerda el orden de tu __init__: id, compania, origen, hora)
            nuevo_avion = Aircraft(id_avion, compania, origen, hora)

            # Lo añadimos al vector
            lista_aviones.append(nuevo_avion)

    # Pasamos a la siguiente línea
    z = z + 1

return lista_aviones