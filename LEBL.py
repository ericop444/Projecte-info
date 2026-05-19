#Primera part
class Gate:
    def __init__(self, name): #li poso un nom
        self.name = name #guardo un nom
        self.occupied = False #comprovo si esta ocupada
        self.aircraft_id = None #quin avió hi ha
class BoardingArea:
    def __init__(self, name, area_type):
        self.name = name #el nom: A,B,C
        self.area_type = area_type  #si es schengen o no schengen
        self.gates = []
class Terminal:
    def __init__(self, name):
        self.name = name
        self.boarding_areas = []
        self.airlines = []
class BarcelonaAP:
    def __init__(self, code):
        self.code = code
        self.terminals = []
def LoadAirlines(terminal, t_name):

    filename = t_name + "_Airlines.txt"

    try:
        f = open(filename, "r")
    except:
        return -1

    terminal.airlines = []

    for line in f:

        parts = line.strip().split()

        if len(parts) == 2:
            airline_code = parts[1]

            terminal.airlines.append(airline_code)
    f.close()


#Inici codi segona part

def SetGates(area, init_gate, end_gate, prefix):
    #Comencem el contador al num d la primera porta
    contador = init_gate

    # El bucle seguira executantse fins que el contador superi l'ultima porta
    while contador <= end_gate:

        nombre_puerta = prefix + str(contador)

        #Creem objecte
        nueva_puerta = Gate(nombre_puerta)

        # L'afegim a la llista de portes de l'area
        area.gates.append(nueva_puerta)

        # Augmentem el contador xq el while acabi
        contador += 1


def LoadAirportStructure(filename):

    # Creem l'objecte principal
    bcn = BarcelonaAP("LEBL")

    try:
        f = open(filename, "r")
        # Llegim totes les línies i les guardem en una llista
        lineas = f.readlines()

        # Bucle de la llista
        i = 0
        while i < len(lineas):
            parts = lineas[i].strip().split()

            # Comprovem si la línia té 6 parts
            if len(parts) >= 6:
                t_name = parts[0]
                area_name = parts[1]
                a_type = parts[2]
                i_gate = int(parts[3])
                e_gate = int(parts[4])
                prefix = parts[5]

                # Busquem si la terminal ja existeix a la llista bcn.terminals
                terminal_actual = None
                j = 0
                # El bucle s'atura si arribem al final o si ja l'hem trobat
                while j < len(bcn.terminals) and terminal_actual == None:
                    if bcn.terminals[j].name == t_name:
                        terminal_actual = bcn.terminals[j]
                    j += 1

                # Si en acabar el while no l'hem trobat, la creem de zero
                if terminal_actual == None:
                    terminal_actual = Terminal(t_name)
                    bcn.terminals.append(terminal_actual)

                # àrea d'embarcament
                nueva_area = BoardingArea(area_name, a_type)

                SetGates(nueva_area, i_gate, e_gate, prefix)

                #Afegim l'àrea a la terminal que toca
                terminal_actual.boarding_areas.append(nueva_area)

            i += 1

        f.close()

        # Carreguem les aerolínies a les terminals
        k = 0
        while k < len(bcn.terminals):
            t = bcn.terminals[k]
            LoadAirlines(t, t.name)
            k += 1

        return bcn

    except FileNotFoundError:
        print("Error: No s'ha trobat el fitxer", filename)
        return None


def IsAirlineInTerminal(terminal, name):
    # Si la terminal es nula, devolvemos False
    if terminal is None:
        return False

    # Si el nombre es nulo, devolvemos False y un código de error
    if name == "":
        return False, -1

    # Si la terminal no tiene aerolíneas, devolvemos False
    if len(terminal.airlines) == 0:
        return False

    i = 0
    encontrada = False
    while i < len(terminal.airlines) and not encontrada:
        if terminal.airlines[i] == name:
            encontrada = True
        i += 1

    return encontrada  # True si está, False si no


def SearchTerminal(bcn, name):
    i = 0
    terminal_encontrada = ""  # String vacío por defecto

    while i < len(bcn.terminals) and terminal_encontrada == "":
        # Usamos la función anterior para revisar cada terminal1
        if IsAirlineInTerminal(bcn.terminals[i], name) == True:
            terminal_encontrada = bcn.terminals[i].name
        i += 1

    return terminal_encontrada  # Devuelve el nombre de la terminal o ""


def GateOccupancy(bcn):
    lista_estado = []

    t = 0
    while t < len(bcn.terminals):
        terminal = bcn.terminals[t]

        a = 0
        while a < len(terminal.boarding_areas):
            area = terminal.boarding_areas[a]

            g = 0
            while g < len(area.gates):
                puerta = area.gates[g]
                # Guardamos: nombre, estado (True/False) e ID del avión[cite: 1]
                datos_puerta = [puerta.name, puerta.occupied, puerta.aircraft_id]
                lista_estado.append(datos_puerta)
                g += 1
            a += 1
        t += 1

    return lista_estado  # Una lista de listas con toda la info[cite: 1]


# Nota: Necesitas IsSchengenAirport definido en airport.py[cite: 1]
from airport import IsSchengenAirport


def AssignGate(bcn, aircraft):
    # 1. Buscamos en qué terminal debe ir según su aerolínea[cite: 1]
    target_terminal_name = SearchTerminal(bcn, aircraft.airline)

    if target_terminal_name == "":
        return -1  # Error: Aerolínea no encontrada en este aeropuerto[cite: 1]

    # 2. Miramos si el vuelo es Schengen o No-Schengen[cite: 1]
    if IsSchengenAirport(aircraft.origin):
        target_type = "Schengen"
    else:
        target_type = "non-Schengen"

    # 3. Buscamos la primera puerta libre en esa terminal y ese tipo de área[cite: 1]
    t = 0
    asignado = False

    while t < len(bcn.terminals) and not asignado:
        if bcn.terminals[t].name == target_terminal_name:

            a = 0
            while a < len(bcn.terminals[t].boarding_areas) and not asignado:
                area = bcn.terminals[t].boarding_areas[a]

                # Comprobamos si el área coincide con el tipo de vuelo[cite: 1]
                if area.type == target_type:

                    g = 0
                    while g < len(area.gates) and not asignado:
                        puerta = area.gates[g]

                        if not puerta.occupied:
                            # ¡ASIGNACIÓN! Actualizamos los datos de la puerta[cite: 1]
                            puerta.occupied = True
                            puerta.aircraft_id = aircraft.id
                            asignado = True
                        g += 1
                a += 1
        t += 1

    if not asignado:
        return -2  # Error: No hay puertas libres de ese tipo[cite: 1]

    return 0  # Éxito[cite: 1]