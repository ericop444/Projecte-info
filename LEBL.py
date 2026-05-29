import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from airport import IsSchengenAirport

# -------------------------------------------------------
# Classe Gate: representa una porta d'embarcament
# -------------------------------------------------------
class Gate:
    def __init__(self, name):
        self.name        = name
        self.occupied    = False
        self.aircraft_id = None


# -------------------------------------------------------
# Classe BoardingArea: representa una zona d'embarcament
# -------------------------------------------------------
class BoardingArea:
    def __init__(self, name, area_type):
        self.name      = name
        self.area_type = area_type   # "Schengen" o "non-Schengen"
        self.gates     = []


# -------------------------------------------------------
# Classe Terminal: representa una terminal de l'aeroport
# -------------------------------------------------------
class Terminal:
    def __init__(self, name):
        self.name           = name
        self.boarding_areas = []
        self.airlines       = []


# -------------------------------------------------------
# Classe BarcelonaAP: representa l'aeroport de Barcelona
# -------------------------------------------------------
class BarcelonaAP:
    def __init__(self, code):
        self.code      = code
        self.terminals = []


# -------------------------------------------------------
# Crea les portes d'una zona d'embarcament
# -------------------------------------------------------
def SetGates(area, init_gate, end_gate, prefix):
    if end_gate <= init_gate:
        return -1

    area.gates = []
    contador = init_gate
    while contador <= end_gate:
        nombre_porta = prefix + str(contador)
        nova_porta   = Gate(nombre_porta)
        area.gates.append(nova_porta)
        contador += 1


# -------------------------------------------------------
# Carrega la llista d'aerolínies d'una terminal des d'un fitxer
# -------------------------------------------------------
def LoadAirlines(terminal, t_name):
    filename = t_name + "_Airlines.txt"

    try:
        f = open(filename, "r")
    except FileNotFoundError:
        print("Error: No s'ha trobat el fitxer", filename)
        return -1

    terminal.airlines = []

    for line in f:
        parts = line.strip().split("\t")
        if len(parts) == 2:
            airline_code = parts[1].strip()
            terminal.airlines.append(airline_code)

    f.close()


# -------------------------------------------------------
# Construeix l'estructura de l'aeroport llegint LEBL.txt
# -------------------------------------------------------
def LoadAirportStructure(filename):
    bcn = BarcelonaAP("LEBL")

    try:
        f     = open(filename, "r")
        lineas = f.readlines()
        f.close()
    except FileNotFoundError:
        print("Error: No s'ha trobat el fitxer", filename)
        return None

    terminal_actual = None
    i = 0

    while i < len(lineas):
        parts = lineas[i].strip().split()

        if len(parts) == 0:
            i += 1
            continue

        if parts[0] == "Terminal":
            t_name          = parts[1]
            terminal_actual = Terminal(t_name)
            bcn.terminals.append(terminal_actual)

        elif parts[0] == "Area" and terminal_actual is not None:
            area_name  = parts[1]
            area_type  = parts[2]
            init_gate  = int(parts[4])
            end_gate   = int(parts[6])
            prefix     = terminal_actual.name + area_name

            nova_area = BoardingArea(area_name, area_type)
            SetGates(nova_area, init_gate, end_gate, prefix)
            terminal_actual.boarding_areas.append(nova_area)

        i += 1

    k = 0
    while k < len(bcn.terminals):
        t = bcn.terminals[k]
        LoadAirlines(t, t.name)
        k += 1

    return bcn


# -------------------------------------------------------
# Retorna una llista amb l'estat de totes les portes
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
                porta       = area.gates[g]
                dades_porta = [porta.name, porta.occupied, porta.aircraft_id]
                llista_estat.append(dades_porta)
                g += 1
            a += 1
        t += 1

    return llista_estat


# -------------------------------------------------------
# Comprova si una aerolínia opera a una terminal determinada
# -------------------------------------------------------
def IsAirlineInTerminal(terminal, name):
    if terminal is None:
        return False

    if name == "" or name is None:
        return False, -1

    if len(terminal.airlines) == 0:
        return False

    i      = 0
    trobada = False
    while i < len(terminal.airlines) and not trobada:
        if terminal.airlines[i] == name:
            trobada = True
        i += 1

    return trobada


# -------------------------------------------------------
# Cerca en quina terminal opera una aerolínia
# -------------------------------------------------------
def SearchTerminal(bcn, name):
    i               = 0
    terminal_trobada = ""

    while i < len(bcn.terminals) and terminal_trobada == "":
        if IsAirlineInTerminal(bcn.terminals[i], name) == True:
            terminal_trobada = bcn.terminals[i].name
        i += 1

    return terminal_trobada


# -------------------------------------------------------
# FUNCIÓ EXTRA
# Comprova si un avió ja té una porta assignada.
# Aquesta funció serveix per evitar que, si l'usuari prem
# dues vegades el botó d'assignar portes, el mateix avió
# pugui ocupar dues portes diferents.
# Retorna True si l'avió ja ocupa alguna porta, i False si no.
# -------------------------------------------------------

def AircraftHasGate(bcn, aircraft_id):
    t = 0
    while t < len(bcn.terminals):
        terminal = bcn.terminals[t]

        a = 0
        while a < len(terminal.boarding_areas):
            area = terminal.boarding_areas[a]

            g = 0
            while g < len(area.gates):
                porta = area.gates[g]

                if porta.occupied and porta.aircraft_id == aircraft_id:
                    return True

                g += 1
            a += 1
        t += 1

    return False

# -------------------------------------------------------
# Assigna una porta a un avió
# Retorna -1 si no es troba aerolínia, -2 si no hi ha portes lliures
# -------------------------------------------------------

def AssignGate(bcn, aircraft):
    # Necessitem aerolínia per assignar porta
    if aircraft.airline is None:
        return -1

    # Si l'avió ja té una porta, no li assignem una altra
    if AircraftHasGate(bcn, aircraft.id):
        return 0

    target_terminal_name = SearchTerminal(bcn, aircraft.airline)

    if target_terminal_name == "":
        return -1

    # Determinem si Schengen o non-Schengen
    if aircraft.origin and IsSchengenAirport(aircraft.origin):
        target_type = "Schengen"
    else:
        target_type = "non-Schengen"

    t        = 0
    assignat = False

    while t < len(bcn.terminals) and not assignat:
        if bcn.terminals[t].name == target_terminal_name:

            a = 0
            while a < len(bcn.terminals[t].boarding_areas) and not assignat:
                area = bcn.terminals[t].boarding_areas[a]

                if area.area_type == target_type:
                    g = 0
                    while g < len(area.gates) and not assignat:
                        porta = area.gates[g]

                        if not porta.occupied:
                            porta.occupied    = True
                            porta.aircraft_id = aircraft.id
                            assignat          = True
                        g += 1
                a += 1
        t += 1

    if not assignat:
        return -2

    return 0


# -------------------------------------------------------
# Allibera la porta ocupada per l'avió amb l'id indicat (v4)
# Retorna -1 si l'avió no es troba en cap porta
# -------------------------------------------------------
def FreeGate(bcn, aircraft_id):
    t = 0
    while t < len(bcn.terminals):
        terminal = bcn.terminals[t]

        a = 0
        while a < len(terminal.boarding_areas):
            area = terminal.boarding_areas[a]

            g = 0
            while g < len(area.gates):
                porta = area.gates[g]

                if porta.occupied and porta.aircraft_id == aircraft_id:
                    porta.occupied    = False
                    porta.aircraft_id = None
                    return 0   # Porta alliberada correctament
                g += 1
            a += 1
        t += 1

    return -1   # Avió no trobat en cap porta


# -------------------------------------------------------
# Assigna portes als avions nocturns (v4)
# Avions que NOMES tenen sortida (sense dades d'arribada)
# Retorna codi -1 si la llista és buida
# -------------------------------------------------------
def AssignNightGates(bcn, aircrafts):
    if not aircrafts:
        print("Error: la llista d'avions és buida")
        return -1

    errors = 0
    i = 0
    while i < len(aircrafts):
        ac = aircrafts[i]

        # Comprovem que és un avió sense arribada (avió nocturn)
        if ac.origin is not None or ac.time is not None:
            i += 1
            continue

        # Necessitem aerolínia per assignar terminal
        if ac.airline is None:
            errors += 1
            i += 1
            continue

        # Per als avions nocturns usem la destinació per determinar el
        # tipus Schengen/non-Schengen (la porta serà de sortida)
        if ac.destination and IsSchengenAirport(ac.destination):
            ac.origin = ac.destination   # temporalment per a AssignGate
        else:
            ac.origin = "XXXX"           # non-Schengen per defecte

        res = AssignGate(bcn, ac)

        # Restaurem l'origen a None
        ac.origin = None

        if res != 0:
            errors += 1
        i += 1

    return errors


# -------------------------------------------------------
# Assigna portes als avions que aterren dins d'una franja horària (v4)
# Allibera prèviament les portes dels avions que ja han sortit
# Retorna el nombre d'avions sense porta assignada en aquella franja
# -------------------------------------------------------
def AssignGatesAtTime(bcn, aircrafts, time):
    # Convertim la franja horària a minuts
    try:
        h, m       = map(int, time.split(':'))
        time_start  = h * 60 + m
        time_end    = time_start + 60
    except ValueError:
        print("Error: format d'hora incorrecte:", time)
        return -1

    # 1. Alliberem les portes dels avions que ja han sortit abans d'ara
    i = 0
    while i < len(aircrafts):
        ac = aircrafts[i]
        if ac.departure_time is not None:
            try:
                dh, dm  = map(int, ac.departure_time.split(':'))
                dep_min = dh * 60 + dm
                if dep_min <= time_start:
                    FreeGate(bcn, ac.id)
            except ValueError:
                pass
        i += 1

    # 2. Assignem porta als avions que aterren en la franja [time_start, time_end)
    no_assignats = 0
    i = 0
    while i < len(aircrafts):
        ac = aircrafts[i]
        if ac.time is not None:
            try:
                ah, am   = map(int, ac.time.split(':'))
                arr_min  = ah * 60 + am
                if time_start <= arr_min < time_end:
                    res = AssignGate(bcn, ac)
                    if res != 0:
                        no_assignats += 1
            except ValueError:
                pass
        i += 1

    return no_assignats


# -------------------------------------------------------
# Genera un gràfic de l'ocupació de portes per terminal i per hora (v4)
# L'estat inicial de bcn ha de correspondre a l'inici del dia
# (només avions nocturns assignats)
# -------------------------------------------------------
def PlotDayOccupancy(bcn, aircrafts):
    hores         = list(range(0, 24))
    hores_labels  = [f"{h:02d}:00" for h in hores]

    # Comptarem les portes ocupades per terminal + no assignats
    n_terminals = len(bcn.terminals)
    # ocupacio[terminal_idx][hora] = nombre de portes ocupades
    ocupacio     = [[0] * 24 for _ in range(n_terminals)]
    no_assignats = [0]       * 24

    # Funció auxiliar per comptar portes ocupades a cada terminal
    def comptar_ocupades():
        llista_comptadors = []
        t = 0
        while t < len(bcn.terminals):
            terminal = bcn.terminals[t]
            comptador = 0
            a = 0
            while a < len(terminal.boarding_areas):
                area = terminal.boarding_areas[a]
                g = 0
                while g < len(area.gates):
                    if area.gates[g].occupied:
                        comptador += 1
                    g += 1
                a += 1
            llista_comptadors.append(comptador)
            t += 1
        return llista_comptadors

    # Simulem hora a hora
    h = 0
    while h < 24:
        time_str = f"{h:02d}:00"
        errors_hora = AssignGatesAtTime(bcn, aircrafts, time_str)
        if errors_hora < 0:
            errors_hora = 0
        no_assignats[h] = errors_hora

        counts = comptar_ocupades()
        t = 0
        while t < n_terminals:
            ocupacio[t][h] = counts[t]
            t += 1
        h += 1

    # --- Dibuixem el gràfic ---
    fig, ax1 = plt.subplots(figsize=(14, 6))

    colors = ['#4f8ef7', '#3ecf8e', '#f0883e', '#a78bfa',
              '#f06292', '#80cbc4', '#ffb74d', '#ce93d8']

    x = list(range(24))
    t = 0
    while t < n_terminals:
        col  = colors[t % len(colors)]
        name = bcn.terminals[t].name
        ax1.plot(x, ocupacio[t], marker='o', color=col,
                 linewidth=2, label=f"Terminal {name}")
        t += 1

    # Barres per als no assignats (eix secundari)
    ax2 = ax1.twinx()
    ax2.bar(x, no_assignats, alpha=0.3, color='red', label='Sense porta')
    ax2.set_ylabel('Vols sense porta assignada', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    ax1.set_xlabel('Hora del dia')
    ax1.set_ylabel('Portes ocupades')
    ax1.set_title('Ocupació de portes per terminal al llarg del dia')
    ax1.set_xticks(x)
    ax1.set_xticklabels(hores_labels, rotation=45, ha='right')
    ax1.legend(loc='upper left')
    ax1.grid(axis='y', alpha=0.4)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + [mpatches.Patch(color='red', alpha=0.3)],
               labels1 + ['Sense porta'], loc='upper left')

    plt.tight_layout()
    plt.show()


# -------------------------------------------------------
# Secció de test
# -------------------------------------------------------
if __name__ == "__main__":
    from aircraft import LoadArrivals, LoadDepartures, MergeMovements, NightAircraft

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
            print(f"  Terminal: {terminal.name} — "
                  f"Aerolínies: {len(terminal.airlines)} — "
                  f"Àrees: {len(terminal.boarding_areas)}")
            t += 1

    # Test 2: GateOccupancy
    print("\n=== Test GateOccupancy (buit) ===")
    if bcn:
        ocupacio = GateOccupancy(bcn)
        lliures  = sum(1 for g in ocupacio if not g[1])
        print(f"Total portes: {len(ocupacio)}, Lliures: {lliures}")

    # Test 3: AssignGate (v3)
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
            print(f"Vols: {len(vols)} — Errors: {errors}")

    # Test 4: FreeGate (v4)
    print("\n=== Test FreeGate ===")
    if bcn and vols:
        id_test = vols[0].id
        res     = FreeGate(bcn, id_test)
        print(f"FreeGate({id_test}): {'OK' if res == 0 else 'ERROR'}")

    # Test 5: Avions nocturns + AssignNightGates (v4)
    print("\n=== Test AssignNightGates ===")
    sortides = LoadDepartures("Departures.txt")
    if sortides and bcn:
        # Reconstruïm bcn net
        bcn2 = LoadAirportStructure("LEBL.txt")
        if bcn2:
            lista_moviments = MergeMovements(LoadArrivals("Arrivals.txt"), sortides)
            if isinstance(lista_moviments, list):
                nocturs = NightAircraft(lista_moviments)
                if isinstance(nocturs, list):
                    errors2 = AssignNightGates(bcn2, nocturs)
                    print(f"Avions nocturns: {len(nocturs)} — Errors: {errors2}")

    # Test 6: AssignGatesAtTime (v4)
    print("\n=== Test AssignGatesAtTime ===")
    if bcn:
        bcn3   = LoadAirportStructure("LEBL.txt")
        vols3  = LoadArrivals("Arrivals.txt")
        if bcn3 and vols3:
            errors_hora = AssignGatesAtTime(bcn3, vols3, "08:00")
            print(f"Franja 08:00 — Sense porta: {errors_hora}")

    # Test 7: PlotDayOccupancy (v4)
    print("\n=== Test PlotDayOccupancy ===")
    if bcn:
        bcn4  = LoadAirportStructure("LEBL.txt")
        vols4 = LoadArrivals("Arrivals.txt")
        if bcn4 and vols4:
            PlotDayOccupancy(bcn4, vols4)