#Classes de prova, aqui va primera part codi

class Gate:
    def __init__(self, name):
        self.name = name

class BoardingArea:
    def __init__(self):
        self.gates = []

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