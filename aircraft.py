class Aircraft:
    def __init__(self, aircraft_id, airline, origin, time):

        self.id = aircraft_id
        self.airline = airline
        self.origin = origin
        self.time = time






































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

