import tkinter as tk
from tkinter import filedialog, messagebox

from airport import *
from aircraft import *
from LEBL import *

# -------------------------------------------------------
# PALETA DE COLORS
# -------------------------------------------------------
BG_DARK     = "#0f1117"
BG_PANEL    = "#1a1d27"
BG_CARD     = "#20243a"
BG_INPUT    = "#2a2d3e"
ACCENT_BLUE = "#4f8ef7"
ACCENT_GRN  = "#3ecf8e"
ACCENT_ORG  = "#f0883e"
ACCENT_PRP  = "#a78bfa"
TEXT_MAIN   = "#e8eaf6"
TEXT_SUB    = "#8892b0"
BORDER      = "#2d3154"

# -------------------------------------------------------
# VARIABLES GLOBALS
# -------------------------------------------------------
airports    = []
aircrafts   = []
bcn_airport = None


# =====================================================
#  WIDGETS PERSONALITZATS
# =====================================================

class HoverButton(tk.Label):
    """Botó personalitzat amb efecte hover"""
    def __init__(self, parent, text, command, color=ACCENT_BLUE, **kwargs):
        super().__init__(
            parent,
            text=text,
            bg=color,
            fg=TEXT_MAIN,
            font=("Consolas", 9, "bold"),
            cursor="hand2",
            pady=8,
            padx=6,
            anchor="w",
            relief="flat",
            **kwargs
        )
        self._color  = color
        self._command = command
        self.bind("<Enter>",   self._on_enter)
        self.bind("<Leave>",   self._on_leave)
        self.bind("<Button-1>", self._on_click)

    def _lighten(self, hex_color, amount=30):
        r = min(255, int(hex_color[1:3], 16) + amount)
        g = min(255, int(hex_color[3:5], 16) + amount)
        b = min(255, int(hex_color[5:7], 16) + amount)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _on_enter(self, e):
        self.config(bg=self._lighten(self._color))

    def _on_leave(self, e):
        self.config(bg=self._color)

    def _on_click(self, e):
        self.config(bg=self._color)
        if self._command:
            self._command()


class Section(tk.Frame):
    """Targeta de secció amb barra lateral de color i capçalera"""
    def __init__(self, parent, title, accent, icon="", **kwargs):
        super().__init__(parent, bg=BG_DARK, **kwargs)

        # Barra lateral de color
        tk.Frame(self, bg=accent, width=4).pack(side="left", fill="y")

        # Contingut interior
        inner = tk.Frame(self, bg=BG_PANEL, pady=12, padx=14)
        inner.pack(side="left", fill="both", expand=True)

        # Capçalera
        hdr = tk.Frame(inner, bg=BG_PANEL)
        hdr.pack(fill="x", pady=(0, 6))
        tk.Label(hdr, text=icon, bg=BG_PANEL, fg=accent,
                 font=("Consolas", 13)).pack(side="left", padx=(0, 8))
        tk.Label(hdr, text=title.upper(), bg=BG_PANEL, fg=accent,
                 font=("Consolas", 10, "bold")).pack(side="left")

        # Línia separadora
        tk.Frame(inner, bg=BORDER, height=1).pack(fill="x", pady=(0, 10))

        # Cos públic
        self.body = tk.Frame(inner, bg=BG_PANEL)
        self.body.pack(fill="x")


class StyledEntry(tk.Frame):
    """Camp d'entrada estilitzat amb etiqueta"""
    def __init__(self, parent, label, **kwargs):
        super().__init__(parent, bg=BG_PANEL, **kwargs)
        tk.Label(self, text=label, bg=BG_PANEL, fg=TEXT_SUB,
                 font=("Consolas", 8), anchor="w").pack(fill="x")
        wrap = tk.Frame(self, bg=BG_INPUT,
                        highlightbackground=BORDER, highlightthickness=1)
        wrap.pack(fill="x", pady=(2, 0))
        self.entry = tk.Entry(
            wrap, bg=BG_INPUT, fg=TEXT_MAIN,
            insertbackground=TEXT_MAIN,
            font=("Consolas", 10),
            relief="flat", bd=5
        )
        self.entry.pack(fill="x")

    def get(self):
        return self.entry.get()

    def delete(self, a, b):
        self.entry.delete(a, b)


class StatusBar(tk.Frame):
    """Barra d'estat inferior"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=BG_CARD, height=28, **kwargs)
        self.pack_propagate(False)
        self._dot = tk.Label(self, text="●", bg=BG_CARD, fg=TEXT_SUB,
                             font=("Consolas", 9))
        self._dot.pack(side="left", padx=(10, 4))
        self._msg = tk.Label(self, text="Llest", bg=BG_CARD, fg=TEXT_SUB,
                             font=("Consolas", 8), anchor="w")
        self._msg.pack(side="left", fill="x", expand=True)
        self._cnt = tk.Label(self, text="", bg=BG_CARD, fg=TEXT_SUB,
                             font=("Consolas", 8))
        self._cnt.pack(side="right", padx=12)

    def set(self, msg, color=TEXT_SUB):
        self._dot.config(fg=color)
        self._msg.config(text=msg, fg=color)

    def update_counters(self, n_ap, n_fl, lebl):
        lebl_txt = "LEBL ✔" if lebl else "LEBL —"
        self._cnt.config(text=f"Aeroports: {n_ap}   Vols: {n_fl}   {lebl_txt}")


# =====================================================
#  FINESTRES EMERGENTS ESTILITZADES
# =====================================================

def _popup_window(title, accent, w=460, h=400):
    win = tk.Toplevel(root)
    win.title(title)
    win.geometry(f"{w}x{h}")
    win.configure(bg=BG_DARK)
    win.resizable(False, False)
    # Capçalera
    hdr = tk.Frame(win, bg=accent, pady=0)
    hdr.pack(fill="x")
    tk.Frame(hdr, bg=accent, height=4).pack(fill="x")
    tk.Label(hdr, text=f"  {title.upper()}", bg=accent, fg="white",
             font=("Consolas", 10, "bold"), pady=8, anchor="w").pack(fill="x")
    return win


def _add_stats_bar(parent, items):
    """Barra de resum amb quadres de colors (label, valor, color)"""
    bar = tk.Frame(parent, bg=BG_DARK, pady=8)
    bar.pack(fill="x")
    for label, val, color in items:
        box = tk.Frame(bar, bg=BG_CARD, padx=14, pady=8)
        box.pack(side="left", padx=8, expand=True)
        tk.Label(box, text=str(val), bg=BG_CARD, fg=color,
                 font=("Consolas", 18, "bold")).pack()
        tk.Label(box, text=label, bg=BG_CARD, fg=TEXT_SUB,
                 font=("Consolas", 7)).pack()


def _add_scrolllist(parent, header, rows, accent):
    """Llista amb scrollbar estilitzada"""
    frame = tk.Frame(parent, bg=BG_CARD,
                     highlightbackground=BORDER, highlightthickness=1)
    frame.pack(fill="both", expand=True, padx=14, pady=(4, 14))
    sb = tk.Scrollbar(frame, bg=BG_PANEL, troughcolor=BG_DARK)
    sb.pack(side="right", fill="y")
    lb = tk.Listbox(
        frame, bg=BG_CARD, fg=TEXT_MAIN,
        selectbackground=accent,
        font=("Consolas", 9),
        bd=0, relief="flat",
        yscrollcommand=sb.set,
        highlightthickness=0
    )
    lb.pack(fill="both", expand=True, padx=6, pady=6)
    sb.config(command=lb.yview)
    lb.insert(tk.END, "  " + header)
    lb.insert(tk.END, "  " + "─" * max(len(header), 40))
    for row in rows:
        lb.insert(tk.END, "  " + row)


def show_airports_popup():
    if not airports:
        messagebox.showerror("Error", "No hi ha aeroports carregats"); return
    n_sch = sum(1 for a in airports if a.isSchengen)
    win = _popup_window("Llista d'Aeroports", ACCENT_BLUE, w=480, h=420)
    _add_stats_bar(win, [
        ("TOTAL",       len(airports),          TEXT_MAIN),
        ("SCHENGEN",    n_sch,                  ACCENT_GRN),
        ("NO SCHENGEN", len(airports) - n_sch,  ACCENT_ORG),
    ])
    rows = []
    i = 0
    while i < len(airports):
        a = airports[i]
        sch = "SI" if a.isSchengen else "NO"
        rows.append(f"{a.code:<8}  {a.lat:>9.4f}  {a.lon:>11.4f}  {sch}")
        i += 1
    _add_scrolllist(win, f"{'ICAO':<8}  {'LAT':>9}  {'LON':>11}  SCH", rows, ACCENT_BLUE)


def show_gates_popup():
    if not bcn_airport:
        messagebox.showerror("Error", "No hi ha estructura de l'aeroport"); return
    gates_list = GateOccupancy(bcn_airport)
    lliures  = sum(1 for g in gates_list if not g[1])
    ocupades = sum(1 for g in gates_list if     g[1])
    win = _popup_window("Ocupació de Portes — LEBL", ACCENT_PRP, w=520, h=460)
    _add_stats_bar(win, [
        ("TOTAL",    len(gates_list), TEXT_MAIN),
        ("LLIURES",  lliures,         ACCENT_GRN),
        ("OCUPADES", ocupades,        ACCENT_ORG),
    ])
    rows = []
    i = 0
    while i < len(gates_list):
        g = gates_list[i]
        estat  = "OCUPADA" if g[1] else "LLIURE "
        avio   = g[2] if g[2] else "—"
        mark   = "●" if g[1] else "○"
        rows.append(f"{mark} {g[0]:<22}  {estat}  {avio}")
        i += 1
    _add_scrolllist(win, f"  {'PORTA':<22}  {'ESTAT':<7}  AVIÓ", rows, ACCENT_PRP)
    status.set(f"Ocupació: {ocupades} ocupades / {lliures} lliures")


# =====================================================
#  LÒGICA DE LES ACCIONS
# =====================================================

def _refresh():
    status.update_counters(len(airports), len(aircrafts), bcn_airport is not None)

# --- Versió 1 ---
def add_airport():
    icao = entry_icao.get().upper()
    if len(icao) != 4 or not icao.isalpha():
        messagebox.showerror("Error", "El codi ICAO ha de tenir 4 lletres"); return
    try:
        lat = float(entry_lat.get())
        lon = float(entry_lon.get())
    except ValueError:
        messagebox.showerror("Error", "Latitud i longitud han de ser nombres"); return
    new_ap = Airport(icao, lat, lon)
    SetSchengen(new_ap)
    if AddAirport(airports, new_ap) == -1:
        messagebox.showerror("Error", f"L'aeroport {icao} ja existeix")
    else:
        status.set(f"✔  Aeroport {icao} afegit  ({len(airports)} total)", ACCENT_GRN)
        entry_icao.delete(0, tk.END)
        entry_lat.delete(0, tk.END)
        entry_lon.delete(0, tk.END)
        _refresh()
        messagebox.showinfo("✔  Aeroport afegit", f"L'aeroport {icao} s'ha afegit correctament.\nTotal aeroports: {len(airports)}")

def remove_airport():
    icao = entry_icao.get().upper()
    if len(icao) != 4:
        messagebox.showerror("Error", "Introdueix un codi ICAO vàlid"); return
    if RemoveAirport(airports, icao) == 0:
        status.set(f"✔  Aeroport {icao} eliminat", ACCENT_GRN)
        entry_icao.delete(0, tk.END)
        _refresh()
        messagebox.showinfo("✔  Aeroport eliminat", f"L'aeroport {icao} s'ha eliminat correctament.")
    else:
        messagebox.showerror("Error", f"No s'ha trobat {icao}")

def load_airports_file():
    fn = filedialog.askopenfilename(title="Selecciona fitxer d'aeroports")
    if not fn: return
    try:
        global airports
        airports = LoadAirports(fn)
        i = 0
        while i < len(airports):
            SetSchengen(airports[i])
            i += 1
        status.set(f"✔  {len(airports)} aeroports carregats", ACCENT_GRN)
        _refresh()
        messagebox.showinfo("✔  Aeroports carregats", f"S'han carregat {len(airports)} aeroports correctament.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def save_schengen():
    if not airports:
        messagebox.showerror("Error", "No hi ha aeroports carregats"); return
    fn = filedialog.asksaveasfilename(defaultextension=".txt")
    if not fn: return
    if SaveSchengenAirports(airports, fn) == -1:
        messagebox.showwarning("Avís", "No hi ha aeroports Schengen")
    else:
        status.set("✔  Aeroports Schengen guardats", ACCENT_GRN)
        messagebox.showinfo("✔  Fitxer guardat", "Els aeroports Schengen s'han guardat correctament.")

def plot_airports_btn():
    if not airports:
        messagebox.showerror("Error", "No hi ha aeroports"); return
    PlotAirports(airports)

def map_airports_btn():
    if not airports:
        messagebox.showerror("Error", "No hi ha aeroports"); return
    MapAirports(airports)
    status.set("✔  Fitxer KML generat", ACCENT_GRN)
    messagebox.showinfo("✔  KML generat", "El fitxer KML dels aeroports s'ha generat correctament.")

# --- Versió 2 ---
def load_arrivals():
    fn = filedialog.askopenfilename(title="Selecciona fitxer d'arribades")
    if not fn: return
    try:
        global aircrafts
        aircrafts = LoadArrivals(fn)
        status.set(f"✔  {len(aircrafts)} vols carregats", ACCENT_GRN)
        _refresh()
        messagebox.showinfo("✔  Vols carregats", f"S'han carregat {len(aircrafts)} vols correctament.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def save_flights_btn():
    if not aircrafts:
        messagebox.showerror("Error", "No hi ha vols"); return
    fn = filedialog.asksaveasfilename(defaultextension=".txt")
    if not fn: return
    if SaveFlights(aircrafts, fn) == 0:
        status.set("✔  Vols guardats", ACCENT_GRN)
        messagebox.showinfo("✔  Vols guardats", "Els vols s'han guardat correctament.")
    else:
        messagebox.showerror("Error", "No s'ha pogut guardar")

def plot_arrivals_btn():
    if not aircrafts:
        messagebox.showerror("Error", "No hi ha vols"); return
    PlotArrivals(aircrafts)

def plot_airlines_btn():
    if not aircrafts:
        messagebox.showerror("Error", "No hi ha vols"); return
    PlotAirlines(aircrafts)

def plot_type_btn():
    if not aircrafts:
        messagebox.showerror("Error", "No hi ha vols"); return
    PlotFlightsType(aircrafts)

def map_flights_btn():
    if not aircrafts:
        messagebox.showerror("Error", "No hi ha vols"); return
    MapFlights(aircrafts)
    status.set("✔  Trajectòries KML generades", ACCENT_GRN)
    messagebox.showinfo("✔  KML generat", "Les trajectòries KML s'han generat correctament.")

def map_long_btn():
    if not aircrafts:
        messagebox.showerror("Error", "No hi ha vols"); return
    long = LongDistanceArrivals(aircrafts)
    if not long:
        messagebox.showinfo("Avís", "No hi ha vols de més de 2000 km"); return
    MapFlights(long)
    status.set(f"✔  {len(long)} vols llarga distància", ACCENT_GRN)
    messagebox.showinfo("✔  KML generat", f"S'han generat les trajectòries de {len(long)} vols de llarga distància.")

# --- Versió 3 ---
def load_lebl():
    fn = filedialog.askopenfilename(title="Selecciona LEBL.txt")
    if not fn: return
    global bcn_airport
    bcn_airport = LoadAirportStructure(fn)
    if bcn_airport:
        status.set("✔  Estructura LEBL carregada", ACCENT_PRP)
        _refresh()
        messagebox.showinfo("✔  LEBL carregat", "L'estructura de l'aeroport LEBL s'ha carregat correctament.")
    else:
        messagebox.showerror("Error", "No s'ha pogut carregar LEBL.txt")

def assign_gates():
    if not bcn_airport:
        messagebox.showerror("Error", "Primer carrega l'estructura LEBL"); return
    if not aircrafts:
        messagebox.showerror("Error", "No hi ha vols carregats"); return
    errors = 0
    i = 0
    while i < len(aircrafts):
        if AssignGate(bcn_airport, aircrafts[i]) != 0:
            errors += 1
        i += 1
    if errors:
        status.set(f"⚠  {errors} vols sense porta", ACCENT_ORG)
        messagebox.showwarning("Avís", f"{errors} vols no han pogut obtenir porta")
    else:
        status.set(f"✔  Totes les portes assignades ({len(aircrafts)} vols)", ACCENT_GRN)
        messagebox.showinfo("✔  Portes assignades", f"Totes les portes s'han assignat correctament.\nTotal vols: {len(aircrafts)}")


# =====================================================
#  CONSTRUCCIÓ DE LA FINESTRA PRINCIPAL
# =====================================================

root = tk.Tk()
root.title("Airport Management  ·  LEBL")
root.geometry("480x840")
root.minsize(480, 600)
root.configure(bg=BG_DARK)
root.resizable(True, True)

# ----------- CAPÇALERA -----------
hdr = tk.Frame(root, bg=BG_PANEL)
hdr.pack(fill="x")
tk.Frame(hdr, bg=ACCENT_BLUE, height=4).pack(fill="x")      # Franja de color

hdr_inner = tk.Frame(hdr, bg=BG_PANEL, pady=12, padx=18)
hdr_inner.pack(fill="x")
tk.Label(hdr_inner, text="✈", bg=BG_PANEL, fg=ACCENT_BLUE,
         font=("Consolas", 20)).pack(side="left", padx=(0, 12))
block = tk.Frame(hdr_inner, bg=BG_PANEL)
block.pack(side="left")
tk.Label(block, text="Airport Management", bg=BG_PANEL, fg=TEXT_MAIN,
         font=("Consolas", 14, "bold"), anchor="w").pack(anchor="w")
tk.Label(block, text="Informatica 1  ·  2025-26 Q2  ·  Barcelona LEBL",
         bg=BG_PANEL, fg=TEXT_SUB, font=("Consolas", 8), anchor="w").pack(anchor="w")

tk.Frame(root, bg=BORDER, height=1).pack(fill="x")

# ----------- ÀREA SCROLLABLE -----------
canvas_scroll = tk.Canvas(root, bg=BG_DARK, highlightthickness=0)
vscroll = tk.Scrollbar(root, orient="vertical", command=canvas_scroll.yview,
                       bg=BG_PANEL, troughcolor=BG_DARK)
canvas_scroll.configure(yscrollcommand=vscroll.set)
vscroll.pack(side="right", fill="y")
canvas_scroll.pack(side="left", fill="both", expand=True)

content = tk.Frame(canvas_scroll, bg=BG_DARK)
cwin = canvas_scroll.create_window((0, 0), window=content, anchor="nw")

content.bind("<Configure>",
    lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all")))
canvas_scroll.bind("<Configure>",
    lambda e: canvas_scroll.itemconfig(cwin, width=e.width))
canvas_scroll.bind_all("<MouseWheel>",
    lambda e: canvas_scroll.yview_scroll(int(-1*(e.delta/120)), "units"))

tk.Frame(content, bg=BG_DARK, height=12).pack()


# =========================================================
#  SECCIÓ 1 — GESTIÓ D'AEROPORTS  (V1)
# =========================================================
sec1 = Section(content, "Gestió d'Aeroports", ACCENT_BLUE, icon="🌍")
sec1.pack(fill="x", padx=16, pady=(0, 10))

# Camps d'entrada en 3 columnes
inputs = tk.Frame(sec1.body, bg=BG_PANEL)
inputs.pack(fill="x", pady=(0, 10))
inputs.columnconfigure(0, weight=1)
inputs.columnconfigure(1, weight=1)
inputs.columnconfigure(2, weight=1)

entry_icao = StyledEntry(inputs, "CODI ICAO")
entry_icao.grid(row=0, column=0, padx=(0, 5), sticky="ew")
entry_lat = StyledEntry(inputs, "LATITUD")
entry_lat.grid(row=0, column=1, padx=5, sticky="ew")
entry_lon = StyledEntry(inputs, "LONGITUD")
entry_lon.grid(row=0, column=2, padx=(5, 0), sticky="ew")

# Graella de botons 2 columnes
g1 = tk.Frame(sec1.body, bg=BG_PANEL)
g1.pack(fill="x")
g1.columnconfigure(0, weight=1)
g1.columnconfigure(1, weight=1)

defs_v1 = [
    ("➕  Afegir aeroport",          add_airport,         ACCENT_BLUE, 0, 0),
    ("🗑  Eliminar aeroport",         remove_airport,      "#c0392b",   0, 1),
    ("📂  Carregar des de fitxer",    load_airports_file,  ACCENT_BLUE, 1, 0),
    ("💾  Guardar Schengen",          save_schengen,       ACCENT_BLUE, 1, 1),
    ("📋  Mostrar llista",            show_airports_popup, ACCENT_BLUE, 2, 0),
    ("📊  Gràfic Schengen/No-Sch.",   plot_airports_btn,   ACCENT_BLUE, 2, 1),
    ("🌐  Mapa Google Earth",         map_airports_btn,    ACCENT_BLUE, 3, 0),
]
for txt, cmd, col, r, c in defs_v1:
    HoverButton(g1, text=txt, command=cmd, color=col).grid(
        row=r, column=c, padx=3, pady=3, sticky="ew")


# =========================================================
#  SECCIÓ 2 — GESTIÓ DE VOLS  (V2)
# =========================================================
sec2 = Section(content, "Gestió de Vols", ACCENT_ORG, icon="🛬")
sec2.pack(fill="x", padx=16, pady=(0, 10))

g2 = tk.Frame(sec2.body, bg=BG_PANEL)
g2.pack(fill="x")
g2.columnconfigure(0, weight=1)
g2.columnconfigure(1, weight=1)

defs_v2 = [
    ("📂  Carregar arribades",         load_arrivals,     ACCENT_ORG, 0, 0),
    ("💾  Guardar vols",               save_flights_btn,  ACCENT_ORG, 0, 1),
    ("📊  Aterratges per hora",        plot_arrivals_btn, ACCENT_ORG, 1, 0),
    ("📊  Vols per companyia",         plot_airlines_btn, ACCENT_ORG, 1, 1),
    ("📊  Schengen vs No-Schengen",    plot_type_btn,     ACCENT_ORG, 2, 0),
    ("🌐  Totes les trajectòries",     map_flights_btn,   ACCENT_ORG, 2, 1),
    ("🌐  Llarga distància (>2000km)", map_long_btn,      ACCENT_ORG, 3, 0),
]
for txt, cmd, col, r, c in defs_v2:
    HoverButton(g2, text=txt, command=cmd, color=col).grid(
        row=r, column=c, padx=3, pady=3, sticky="ew")


# =========================================================
#  SECCIÓ 3 — GESTIÓ DE PORTES  (V3)
# =========================================================
sec3 = Section(content, "Gestió de Portes — LEBL", ACCENT_PRP, icon="🚪")
sec3.pack(fill="x", padx=16, pady=(0, 10))

g3 = tk.Frame(sec3.body, bg=BG_PANEL)
g3.pack(fill="x")
g3.columnconfigure(0, weight=1)
g3.columnconfigure(1, weight=1)

defs_v3 = [
    ("📂  Carregar estructura LEBL",  load_lebl,        ACCENT_PRP, 0, 0),
    ("🚪  Assignar portes als vols",  assign_gates,     ACCENT_PRP, 0, 1),
    ("📋  Mostrar ocupació portes",   show_gates_popup, ACCENT_PRP, 1, 0),
]
for txt, cmd, col, r, c in defs_v3:
    HoverButton(g3, text=txt, command=cmd, color=col).grid(
        row=r, column=c, padx=3, pady=3, sticky="ew")

tk.Frame(content, bg=BG_DARK, height=10).pack()


# ----------- BARRA D'ESTAT INFERIOR -----------
tk.Frame(root, bg=BORDER, height=1).pack(fill="x", side="bottom")
status = StatusBar(root)
status.pack(fill="x", side="bottom")
status.set("Llest — carrega un fitxer per començar")
_refresh()

root.mainloop()

#creacio v.4