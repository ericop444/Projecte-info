import tkinter as tk
from tkinter import filedialog, messagebox
from airport import *
from aircraft import * # ¡FALTABA ESTO!
import matplotlib.pyplot as plt

# principal
root = tk.Tk()
root.title("Gestión de Aeropuertos")
root.geometry("450x850")

# lista de aeropuertos
airports = []
aircrafts = []

def add_airport():
    icaocode = entry_icao.get().upper()
    try:
        lat = float(entry_lat.get())
        lon = float(entry_lon.get())
    except ValueError:
        messagebox.showerror("Error", "Latitud y longitud deben ser números")
        return

    if len(icaocode) != 4 or not icaocode.isalpha():
        messagebox.showerror("Error", "El código ICAO debe tener 4 letras")
        return

    new_airport = Airport(icaocode, lat, lon)
    SetSchengen(new_airport)

    result = AddAirport(airports, new_airport)
    if result == -1:
        messagebox.showerror("Error", f"El aeropuerto {icaocode} ya existe.")
    else:
        messagebox.showinfo("Éxito", f"Aeropuerto {icaocode} agregado correctamente")
        entry_icao.delete(0, tk.END)
        entry_lat.delete(0, tk.END)
        entry_lon.delete(0, tk.END)

def remove_airport():
    icaocode = entry_icao.get().upper()
    if len(icaocode) != 4:
        messagebox.showerror("Error", "Introduce un código ICAO válido")
        return

    result = RemoveAirport(airports, icaocode)
    if result == 0:
        messagebox.showinfo("Éxito", f"Aeropuerto {icaocode} eliminado correctamente")
        entry_icao.delete(0, tk.END)
    else:
        messagebox.showerror("Error", f"No se encontró el aeropuerto {icaocode}")

def load_airports_file():
    filename = filedialog.askopenfilename(title="Selecciona archivo de aeropuertos")
    if not filename:
        return
    try:
        global airports
        airports = LoadAirports(filename)
        i = 0
        while i < len(airports):
            SetSchengen(airports[i])
            i += 1
        messagebox.showinfo("Éxito", f"Cargados {len(airports)} aeropuertos desde el archivo")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")

def save_schengen_airports():
    if not airports:
        messagebox.showerror("Error", "No hay aeropuertos cargados")
        return
    filename = filedialog.asksaveasfilename(title="Guardar aeropuertos Schengen", defaultextension=".txt")
    if not filename:
        return
    try:
        result = SaveSchengenAirports(airports, filename)
        if result == -1:
            messagebox.showwarning("Aviso", "No se guardó el archivo (tal vez no hay aeropuertos Schengen).")
        else:
            messagebox.showinfo("Éxito", f"Aeropuertos Schengen guardados en {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

def show_airports():
    if not airports:
        messagebox.showerror("Error", "No hay aeropuertos cargados")
        return
    info = ""
    i = 0
    while i < len(airports):
        ap = airports[i]
        info += f"{ap.code} - Lat: {ap.lat:.4f}, Lon: {ap.lon:.4f}, Schengen: {ap.isSchengen}\n"
        i += 1
    messagebox.showinfo("Lista de Aeropuertos", info)

def plot_airports():
    if not airports:
        messagebox.showerror("Error", "No hay aeropuertos para graficar")
        return
    try:
        PlotAirports(airports)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo mostrar gráfico:\n{e}")

def map_airports():
    if not airports:
        messagebox.showerror("Error", "No hay aeropuertos para mostrar en Google Earth")
        return
    try:
        MapAirports(airports)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir Google Earth:\n{e}")

def load_arrivals_file():
    filename = filedialog.askopenfilename(title="Selecciona archivo de llegadas (Arrivals.txt)")
    if not filename: return
    try:
        global aircrafts
        aircrafts = LoadArrivals(filename)
        messagebox.showinfo("Éxito", f"Cargados {len(aircrafts)} vuelos de llegada")
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar llegadas:\n{e}")

def save_aircrafts_file():
    if not aircrafts:
        messagebox.showerror("Error", "No hay vuelos cargados")
        return
    filename = filedialog.asksaveasfilename(title="Guardar información de vuelos", defaultextension=".txt")
    if not filename: return
    SaveFlights(aircrafts, filename)
    messagebox.showinfo("Éxito", "Vuelos guardados correctamente")

def plot_arrivals_hour():
    if not aircrafts:
        messagebox.showerror("Error", "No hay vuelos")
        return
    PlotArrivals(aircrafts)

def plot_arrivals_airline():
    if not aircrafts:
        messagebox.showerror("Error", "No hay vuelos")
        return
    PlotAirlines(aircrafts)

def plot_arrivals_type():
    if not aircrafts:
        messagebox.showerror("Error", "No hay vuelos")
        return
    PlotFlightsType(aircrafts)

def map_all_trajectories():
    if not aircrafts:
        messagebox.showerror("Error", "No hay vuelos")
        return
    MapFlights(aircrafts)

def map_long_trajectories():
    if not aircrafts:
        messagebox.showerror("Error", "No hay vuelos")
        return
    long_dist_flights = LongDistanceArrivals(aircrafts)
    if not long_dist_flights:
        messagebox.showinfo("Aviso", "No hay vuelos de más de 2000km")
        return
    MapFlights(long_dist_flights)

# entradas
tk.Label(root, text="Código ICAO:").pack(pady=(10, 0))
entry_icao = tk.Entry(root)
entry_icao.pack()

tk.Label(root, text="Latitud:").pack()
entry_lat = tk.Entry(root)
entry_lat.pack()

tk.Label(root, text="Longitud:").pack()
entry_lon = tk.Entry(root)
entry_lon.pack()

# Botones de la version 1
tk.Button(root, text="Agregar aeropuerto", width=35, command=add_airport).pack(pady=(15, 5))
tk.Button(root, text="Eliminar aeropuerto", width=35, command=remove_airport).pack(pady=5)
tk.Button(root, text="Cargar aeropuertos desde archivo", width=35, command=load_airports_file).pack(pady=5)
tk.Button(root, text="Guardar aeropuertos Schengen", width=35, command=save_schengen_airports).pack(pady=5)
tk.Button(root, text="Mostrar aeropuertos", width=35, command=show_airports).pack(pady=5)
tk.Button(root, text="Graficar aeropuertos", width=35, command=plot_airports).pack(pady=5)
tk.Button(root, text="Mostrar aeropuertos en Google Earth", width=35, command=map_airports).pack(pady=5)

# Botones de la versión 2 (¡CORREGIDOS NOMBRES!)
tk.Button(root, text="Cargar llegadas", width=35, command=load_arrivals_file).pack(pady=5)
tk.Button(root, text="Guardar vuelos", width=35, command=save_aircrafts_file).pack(pady=5)
tk.Button(root, text="Graficar llegadas por hora", width=35, command=plot_arrivals_hour).pack(pady=5)
tk.Button(root, text="Graficar vuelos por compañía", width=35, command=plot_arrivals_airline).pack(pady=5)
tk.Button(root, text="Graficar Schengen vs No-Schengen", width=35, command=plot_arrivals_type).pack(pady=5)
tk.Button(root, text="Mostrar trayectorias en Google Earth", width=35, command=map_all_trajectories).pack(pady=5)
tk.Button(root, text="Mostrar solo larga distancia en Google Earth", width=35, command=map_long_trajectories).pack(pady=5)

root.mainloop()