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