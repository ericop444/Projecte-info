import tkinter as tk
from tkinter import filedialog, messagebox
from airport import *
from aircraft import *
from LEBL import *

# -------------------------------------------------------
# Finestra principal de l'aplicació
# -------------------------------------------------------
root = tk.Tk()
root.title("Gestió d'Aeroports")
root.geometry("470x950")

# Variables globals: llistes i l'estructura de l'aeroport
airports = []
aircrafts = []
bcn_airport = None  # Objecte BarcelonaAP (carregat des de LEBL.txt)


# -------------------------------------------------------
# FUNCIONS VERSIÓ 1: gestió d'aeroports
# -------------------------------------------------------

def add_airport():
    icaocode = entry_icao.get().upper()

    # Comprovem que el codi ICAO tingui exactament 4 lletres
    if len(icaocode) != 4 or not icaocode.isalpha():
        messagebox.showerror("Error", "El codi ICAO ha de tenir 4 lletres")
        return

    try:
        lat = float(entry_lat.get())
        lon = float(entry_lon.get())
    except ValueError:
        messagebox.showerror("Error", "Latitud i longitud han de ser nombres")
        return

    new_airport = Airport(icaocode, lat, lon)
    SetSchengen(new_airport)

    result = AddAirport(airports, new_airport)
    if result == -1:
        messagebox.showerror("Error", f"L'aeroport {icaocode} ja existeix.")
    else:
        messagebox.showinfo("Èxit", f"Aeroport {icaocode} afegit correctament")
        entry_icao.delete(0, tk.END)
        entry_lat.delete(0, tk.END)
        entry_lon.delete(0, tk.END)


def remove_airport():
    icaocode = entry_icao.get().upper()

    if len(icaocode) != 4:
        messagebox.showerror("Error", "Introdueix un codi ICAO vàlid")
        return

    result = RemoveAirport(airports, icaocode)
    if result == 0:
        messagebox.showinfo("Èxit", f"Aeroport {icaocode} eliminat correctament")
        entry_icao.delete(0, tk.END)
    else:
        messagebox.showerror("Error", f"No s'ha trobat l'aeroport {icaocode}")


def load_airports_file():
    filename = filedialog.askopenfilename(title="Selecciona fitxer d'aeroports")
    if not filename:
        return

    try:
        global airports
        airports = LoadAirports(filename)

        # Actualitzem l'atribut Schengen de cada aeroport
        i = 0
        while i < len(airports):
            SetSchengen(airports[i])
            i += 1

        messagebox.showinfo("Èxit", f"Carregats {len(airports)} aeroports des del fitxer")
    except Exception as e:
        messagebox.showerror("Error", f"No s'ha pogut carregar el fitxer:\n{e}")


def save_schengen_airports():
    if not airports:
        messagebox.showerror("Error", "No hi ha aeroports carregats")
        return

    filename = filedialog.asksaveasfilename(title="Guardar aeroports Schengen", defaultextension=".txt")
    if not filename:
        return

    try:
        result = SaveSchengenAirports(airports, filename)
        if result == -1:
            messagebox.showwarning("Avís", "No s'ha guardat el fitxer (potser no hi ha aeroports Schengen).")
        else:
            messagebox.showinfo("Èxit", f"Aeroports Schengen guardats a {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"No s'ha pogut guardar el fitxer:\n{e}")


def show_airports():
    if not airports:
        messagebox.showerror("Error", "No hi ha aeroports carregats")
        return

    info = ""
    i = 0
    while i < len(airports):
        ap = airports[i]
        info += f"{ap.code} - Lat: {ap.lat:.4f}, Lon: {ap.lon:.4f}, Schengen: {ap.isSchengen}\n"
        i += 1

    messagebox.showinfo("Llista d'Aeroports", info)


def plot_airports():
    if not airports:
        messagebox.showerror("Error", "No hi ha aeroports per graficar")
        return
    try:
        PlotAirports(airports)
    except Exception as e:
        messagebox.showerror("Error", f"No s'ha pogut mostrar el gràfic:\n{e}")


def map_airports():
    if not airports:
        messagebox.showerror("Error", "No hi ha aeroports per mostrar a Google Earth")
        return
    try:
        MapAirports(airports)
    except Exception as e:
        messagebox.showerror("Error", f"No s'ha pogut obrir Google Earth:\n{e}")


# -------------------------------------------------------
# FUNCIONS VERSIÓ 2: gestió de vols
# -------------------------------------------------------

def load_arrivals_file():
    filename = filedialog.askopenfilename(title="Selecciona fitxer d'arribades (Arrivals.txt)")
    if not filename:
        return
    try:
        global aircrafts
        aircrafts = LoadArrivals(filename)
        messagebox.showinfo("Èxit", f"Carregats {len(aircrafts)} vols d'arribada")
    except Exception as e:
        messagebox.showerror("Error", f"Error al carregar arribades:\n{e}")


def save_aircrafts_file():
    if not aircrafts:
        messagebox.showerror("Error", "No hi ha vols carregats")
        return
    filename = filedialog.asksaveasfilename(title="Guardar informació de vols", defaultextension=".txt")
    if not filename:
        return
    result = SaveFlights(aircrafts, filename)
    if result == 0:
        messagebox.showinfo("Èxit", "Vols guardats correctament")
    else:
        messagebox.showerror("Error", "No s'ha pogut guardar el fitxer")


def plot_arrivals_hour():
    if not aircrafts:
        messagebox.showerror("Error", "No hi ha vols carregats")
        return
    PlotArrivals(aircrafts)


def plot_arrivals_airline():
    if not aircrafts:
        messagebox.showerror("Error", "No hi ha vols carregats")
        return
    PlotAirlines(aircrafts)


def plot_arrivals_type():
    if not aircrafts:
        messagebox.showerror("Error", "No hi ha vols carregats")
        return
    PlotFlightsType(aircrafts)


def map_all_trajectories():
    if not aircrafts:
        messagebox.showerror("Error", "No hi ha vols carregats")
        return
    MapFlights(aircrafts)


def map_long_trajectories():
    if not aircrafts:
        messagebox.showerror("Error", "No hi ha vols carregats")
        return
    long_dist_flights = LongDistanceArrivals(aircrafts)
    if not long_dist_flights:
        messagebox.showinfo("Avís", "No hi ha vols de més de 2000 km")
        return
    MapFlights(long_dist_flights)


# -------------------------------------------------------
# FUNCIONS VERSIÓ 3: gestió de portes (LEBL)
# -------------------------------------------------------

def load_bcn_structure():
    filename = filedialog.askopenfilename(title="Selecciona estructura de l'aeroport (LEBL.txt)")
    if not filename:
        return
    try:
        global bcn_airport
        bcn_airport = LoadAirportStructure(filename)
        if bcn_airport is not None:
            messagebox.showinfo("Èxit", "Estructura de l'aeroport carregada correctament")
        else:
            messagebox.showerror("Error", "No s'ha pogut carregar el fitxer LEBL.txt")
    except Exception as e:
        messagebox.showerror("Error", f"No s'ha pogut carregar l'estructura:\n{e}")


def assign_gates_v3():
    # Comprovem que tenim l'estructura i els vols carregats
    if not bcn_airport:
        messagebox.showerror("Error", "Primer has de carregar l'estructura de l'aeroport")
        return
    if not aircrafts:
        messagebox.showerror("Error", "No hi ha vols (arribades) carregats")
        return

    # Assignem portes a cada avió de la llista
    i = 0
    count_errors = 0
    while i < len(aircrafts):
        result = AssignGate(bcn_airport, aircrafts[i])
        if result != 0:
            count_errors += 1
        i += 1

    if count_errors > 0:
        messagebox.showwarning("Avís", f"Procés finalitzat. {count_errors} vols no han pogut obtenir porta.")
    else:
        messagebox.showinfo("Èxit", "Portes assignades a tots els vols correctament")


def show_gates_occupancy():
    if not bcn_airport:
        messagebox.showerror("Error", "No hi ha dades de l'aeroport")
        return

    gates_list = GateOccupancy(bcn_airport)

    # Comptem quantes portes estan lliures i ocupades
    lliures = 0
    ocupades = 0
    k = 0
    while k < len(gates_list):
        if gates_list[k][1]:
            ocupades += 1
        else:
            lliures += 1
        k += 1

    # Mostrem un resum i les primeres portes ocupades
    info = f"Total portes: {len(gates_list)}\nLliures: {lliures} | Ocupades: {ocupades}\n\n"
    info += "Portes ocupades:\n"

    i = 0
    mostrades = 0
    while i < len(gates_list) and mostrades < 20:
        porta = gates_list[i]
        # porta[0]=nom, porta[1]=ocupada, porta[2]=id_avió
        if porta[1]:
            info += f"Porta: {porta[0]} - OCUPADA ({porta[2]})\n"
            mostrades += 1
        i += 1

    if mostrades == 20:
        info += "...(llista truncada, massa portes per mostrar)..."

    messagebox.showinfo("Ocupació de Portes", info)


# -------------------------------------------------------
# WIDGETS DE LA INTERFÍCIE
# -------------------------------------------------------

# Camps d'entrada per a la versió 1
tk.Label(root, text="Codi ICAO:").pack(pady=(10, 0))
entry_icao = tk.Entry(root)
entry_icao.pack()

tk.Label(root, text="Latitud:").pack()
entry_lat = tk.Entry(root)
entry_lat.pack()

tk.Label(root, text="Longitud:").pack()
entry_lon = tk.Entry(root)
entry_lon.pack()

# Botons de la versió 1
tk.Label(root, text="--- Gestió d'Aeroports (V1) ---", fg="darkgreen").pack(pady=(10, 0))
tk.Button(root, text="Afegir aeroport", width=38, command=add_airport).pack(pady=(5, 2))
tk.Button(root, text="Eliminar aeroport", width=38, command=remove_airport).pack(pady=2)
tk.Button(root, text="Carregar aeroports des de fitxer", width=38, command=load_airports_file).pack(pady=2)
tk.Button(root, text="Guardar aeroports Schengen", width=38, command=save_schengen_airports).pack(pady=2)
tk.Button(root, text="Mostrar aeroports", width=38, command=show_airports).pack(pady=2)
tk.Button(root, text="Graficar aeroports", width=38, command=plot_airports).pack(pady=2)
tk.Button(root, text="Mostrar aeroports a Google Earth", width=38, command=map_airports).pack(pady=2)

# Botons de la versió 2
tk.Label(root, text="--- Gestió de Vols (V2) ---", fg="darkorange").pack(pady=(10, 0))
tk.Button(root, text="Carregar arribades", width=38, command=load_arrivals_file).pack(pady=2)
tk.Button(root, text="Guardar vols", width=38, command=save_aircrafts_file).pack(pady=2)
tk.Button(root, text="Graficar arribades per hora", width=38, command=plot_arrivals_hour).pack(pady=2)
tk.Button(root, text="Graficar vols per companyia", width=38, command=plot_arrivals_airline).pack(pady=2)
tk.Button(root, text="Graficar Schengen vs No-Schengen", width=38, command=plot_arrivals_type).pack(pady=2)
tk.Button(root, text="Mostrar trajectòries a Google Earth", width=38, command=map_all_trajectories).pack(pady=2)
tk.Button(root, text="Mostrar llarga distància a Google Earth", width=38, command=map_long_trajectories).pack(pady=2)

# Botons de la versió 3
tk.Label(root, text="--- Gestió de Portes (V3) ---", fg="blue").pack(pady=(10, 0))
tk.Button(root, text="Carregar estructura aeroport (LEBL.txt)", width=38, command=load_bcn_structure).pack(pady=2)
tk.Button(root, text="Assignar portes als vols", width=38, command=assign_gates_v3).pack(pady=2)
tk.Button(root, text="Mostrar ocupació de portes", width=38, command=show_gates_occupancy).pack(pady=2)

# Iniciem el bucle principal de la interfície
root.mainloop()