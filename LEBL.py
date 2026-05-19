from airport import IsSchengenAirport

# -------------------------------------------------------
# Classe Gate: representa una porta d'embarcament
# Guarda el nom, si està ocupada i quin avió hi ha
# -------------------------------------------------------
class Gate:
    def __init__(self, name):
        self.name = name
        self.occupied = False       # Per defecte la porta és lliure
        self.aircraft_id = None     # Cap avió assignat inicialment


# -------------------------------------------------------
# Classe BoardingArea: representa una zona d'embarcament
# Guarda el nom, el tipus (Schengen/non-Schengen) i la llista de portes
# -------------------------------------------------------
class BoardingArea:
    def __init__(self, name, area_type):
        self.name = name            # Per exemple: A, B, C...
        self.area_type = area_type  # "Schengen" o "non-Schengen"
        self.gates = []             # Llista d'objectes Gate


# -------------------------------------------------------
# Classe Terminal: representa una terminal de l'aeroport
# Guarda el nom, les zones d'embarcament i les aerolínies que hi operen
# -------------------------------------------------------
class Terminal:
    def __init__(self, name):
        self.name = name
        self.boarding_areas = []    # Llista d'objectes BoardingArea
        self.airlines = []          # Llista de codis ICAO de les aerolínies


# -------------------------------------------------------
# Classe BarcelonaAP: representa l'aeroport de Barcelona (LEBL)
# Guarda el codi ICAO i la llista de terminals
# -------------------------------------------------------
class BarcelonaAP:
    def __init__(self, code):
        self.code = code
        self.terminals = []         # Llista d'objectes Terminal


# -------------------------------------------------------
# Crea les portes d'una zona d'embarcament
# des de init_gate fins a end_gate amb el prefix donat
# Retorna -1 si end_gate no és major que init_gate
# -------------------------------------------------------
def SetGates(area, init_gate, end_gate, prefix):
    # Comprovem que el rang és vàlid
    if end_gate <= init_gate:
        return -1

    # Esborrem la llista anterior de portes
    area.gates = []

    contador = init_gate
    while contador <= end_gate:
        # El nom de la porta és el prefix + el número
        nombre_porta = prefix + str(contador)
        nova_porta = Gate(nombre_porta)
        area.gates.append(nova_porta)
        contador += 1


# -------------------------------------------------------
# Carrega la llista d'aerolínies d'una terminal des d'un fitxer
# El fitxer ha de tenir format: NomAerolínia<TAB>CodiICAO
# Retorna -1 si el fitxer no existeix
# -------------------------------------------------------
def LoadAirlines(terminal, t_name):
    filename = t_name + "_Airlines.txt"

    try:
        f = open(filename, "r")
    except FileNotFoundError:
        print("Error: No s'ha trobat el fitxer", filename)
        return -1

    # Esborrem la llista anterior d'aerolínies
    terminal.airlines = []

    for line in f:
        # El format és: Nom<TAB>Codi (separats per tabulació)
        parts = line.strip().split("\t")

        if len(parts) == 2:
            airline_code = parts[1].strip()   # Agafem el codi ICAO (segona columna)
            terminal.airlines.append(airline_code)

    f.close()


# -------------------------------------------------------
# Construeix l'estructura de l'aeroport llegint el fitxer LEBL.txt
# Crida a SetGates i LoadAirlines per completar l'estructura
# Retorna None si el fitxer no existeix
# -------------------------------------------------------
def LoadAirportStructure(filename):
    # Creem l'objecte principal de l'aeroport
    bcn = BarcelonaAP("LEBL")

    try:
        f = open(filename, "r")
        lineas = f.readlines()
        f.close()
    except FileNotFoundError:
        print("Error: No s'ha trobat el fitxer", filename)
        return None

    terminal_actual = None
    i = 0

    while i < len(lineas):
        parts = lineas[i].strip().split()

        # Saltem línies buides
        if len(parts) == 0:
            i += 1
            continue

        # Línia de terminal: "Terminal T1 5 boarding areas"
        if parts[0] == "Terminal":
            t_name = parts[1]
            terminal_actual = Terminal(t_name)
            bcn.terminals.append(terminal_actual)

        # Línia d'àrea: "Area A Schengen Gates 1 - 11"
        elif parts[0] == "Area" and terminal_actual is not None:
            # Exemple: Area A Schengen Gates 1 - 11
            # parts: [Area, A, Schengen/non-Schengen, Gates, 1, -, 11]
            area_name = parts[1]

            # El tipus pot ser "Schengen" o "non-Schengen"
            area_type = parts[2]

            # Els números de porta estan a les posicions 4 i 6
            init_gate = int(parts[4])
            end_gate = int(parts[6])

            # El prefix és el nom de la terminal + l'àrea (ex: T1A)
            prefix = terminal_actual.name + area_name

            # Creem l'àrea i li assignem les portes
            nova_area = BoardingArea(area_name, area_type)
            SetGates(nova_area, init_gate, end_gate, prefix)
            terminal_actual.boarding_areas.append(nova_area)

        i += 1

    # Carreguem les aerolínies de cada terminal
    k = 0
    while k < len(bcn.terminals):
        t = bcn.terminals[k]
        LoadAirlines(t, t.name)
        k += 1

    return bcn


# -------------------------------------------------------
# Comprova si una aerolínia opera a una terminal determinada
# Retorna False si la terminal no té aerolínies o el nom és buit
# Retorna False i codi d'error -1 si el nom és null/buit
# -------------------------------------------------------
def IsAirlineInTerminal(terminal, name):
    # Si la terminal és nul·la, retornem False
    if terminal is None:
        return False

    # Si el nom és buit, retornem False i codi d'error
    if name == "" or name is None:
        return False, -1

    # Si la terminal no té aerolínies, retornem False
    if len(terminal.airlines) == 0:
        return False

    i = 0
    trobada = False
    while i < len(terminal.airlines) and not trobada:
        if terminal.airlines[i] == name:
            trobada = True
        i += 1

    return trobada  # True si hi és, False si no


# -------------------------------------------------------
# Cerca en quina terminal opera una aerolínia
# Retorna el nom de la terminal o string buit si no es troba
# -------------------------------------------------------
def SearchTerminal(bcn, name):
    i = 0
    terminal_trobada = ""  # Per defecte string buit

    while i < len(bcn.terminals) and terminal_trobada == "":
        # Usem IsAirlineInTerminal per comprovar cada terminal
        if IsAirlineInTerminal(bcn.terminals[i], name) == True:
            terminal_trobada = bcn.terminals[i].name
        i += 1

    return terminal_trobada  # Retorna el nom o ""


# -------------------------------------------------------
# Retorna una llista amb l'estat de totes les portes:
# cada element és [nom_porta, ocupada, id_avió]
# -------------------------------------------------------
def GateOccupancy(bcn):
    llista_estat = []

    t = 0
    while t < len(bcn.terminals):
        terminal = bcn.terminals[t]

        a = 0
        while a < len(terminal.boarding_areas):
            area = terminal.boarding_areas[a]

            g = 0
            while g < len(area.gates):
                porta = area.gates[g]
                # Guardem: nom, estat (True/False) i ID de l'avió
                dades_porta = [porta.name, porta.occupied, porta.aircraft_id]
                llista_estat.append(dades_porta)
                g += 1
            a += 1
        t += 1

    return llista_estat


# -------------------------------------------------------
# Assigna una porta a un avió:
# 1. Busca la terminal de l'aerolínia
# 2. Comprova si el vol és Schengen o No-Schengen
# 3. Assigna la primera porta lliure del tipus correcte
# Retorna -1 si no es troba aerolínia, -2 si no hi ha portes lliures
# -------------------------------------------------------
def AssignGate(bcn, aircraft):
    # 1. Busquem a quina terminal va l'aerolínia
    target_terminal_name = SearchTerminal(bcn, aircraft.airline)

    if target_terminal_name == "":
        return -1  # Error: aerolínia no trobada en cap terminal

    # 2. Comprovem si el vol ve d'un país Schengen
    if IsSchengenAirport(aircraft.origin):
        target_type = "Schengen"
    else:
        target_type = "non-Schengen"

    # 3. Busquem la primera porta lliure a la terminal i tipus correctes
    t = 0
    assignat = False

    while t < len(bcn.terminals) and not assignat:
        if bcn.terminals[t].name == target_terminal_name:

            a = 0
            while a < len(bcn.terminals[t].boarding_areas) and not assignat:
                area = bcn.terminals[t].boarding_areas[a]

                # Comprovem que l'àrea és del tipus correcte (Schengen/non-Schengen)
                # CORRECCIÓ: usem area.area_type (no area.type)
                if area.area_type == target_type:

                    g = 0
                    while g < len(area.gates) and not assignat:
                        porta = area.gates[g]

                        if not porta.occupied:
                            # Assignem la porta: marquem com ocupada i guardem l'id de l'avió
                            porta.occupied = True
                            porta.aircraft_id = aircraft.id
                            assignat = True
                        g += 1
                a += 1
        t += 1

    if not assignat:
        return -2  # Error: no hi ha portes lliures del tipus necessari

    return 0  # Assignació correcta


# -------------------------------------------------------
# Secció de test: s'executa només quan correm LEBL.py directament
# -------------------------------------------------------
if __name__ == "__main__":
    from aircraft import LoadArrivals

    # Test 1: Carreguem l'estructura de l'aeroport
    print("=== Test LoadAirportStructure ===")
    bcn = LoadAirportStructure("LEBL.txt")
    if bcn is None:
        print("Error carregant LEBL.txt")
    else:
        print(f"Aeroport: {bcn.code}")
        t = 0
        while t < len(bcn.terminals):
            terminal = bcn.terminals[t]
            print(f"  Terminal: {terminal.name} - Aerolínies: {len(terminal.airlines)} - Àrees: {len(terminal.boarding_areas)}")
            t += 1

    # Test 2: IsAirlineInTerminal
    print("\n=== Test IsAirlineInTerminal ===")
    if bcn and len(bcn.terminals) > 0:
        result = IsAirlineInTerminal(bcn.terminals[0], "VLG")
        print(f"VLG a {bcn.terminals[0].name}:", result)

    # Test 3: SearchTerminal
    print("\n=== Test SearchTerminal ===")
    if bcn:
        terminal_vlg = SearchTerminal(bcn, "VLG")
        print(f"Terminal de VLG: {terminal_vlg}")

    # Test 4: GateOccupancy (abans d'assignar portes)
    print("\n=== Test GateOccupancy (buit) ===")
    if bcn:
        ocupacio = GateOccupancy(bcn)
        lliures = 0
        k = 0
        while k < len(ocupacio):
            if not ocupacio[k][1]:
                lliures += 1
            k += 1
        print(f"Total portes: {len(ocupacio)}, Lliures: {lliures}")

    # Test 5: AssignGate
    print("\n=== Test AssignGate ===")
    if bcn:
        vols = LoadArrivals("Arrivals.txt")
        if vols:
            errors = 0
            i = 0
            while i < len(vols):
                res = AssignGate(bcn, vols[i])
                if res != 0:
                    errors += 1
                i += 1
            print(f"Vols assignats: {len(vols) - errors}, Errors: {errors}")

            # Mostrem ocupació actualitzada
            ocupacio = GateOccupancy(bcn)
            ocupades = 0
            k = 0
            while k < len(ocupacio):
                if ocupacio[k][1]:
                    ocupades += 1
                k += 1
            print(f"Portes ocupades ara: {ocupades}")