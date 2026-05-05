#Classes de prova, aqui va primera part codi

class Gate:
    def __init__(self, name):
        self.name = name

class BoardingArea:
    def __init__(self):
        self.gates = []

#Inici codi segona part
def SetGates(area, init_gate, end_gate, prefix):
    # Inicializamos nuestro contador en el número de la primera puerta
    contador = init_gate

    # El bucle seguirá ejecutándose fins que el contador superi l'ultima porta
    while contador <= end_gate:

        nombre_puerta = prefix + str(contador)

        # 2. Creamos el objeto Gate (usando la clase que hará el Integrante 1)
        nueva_puerta = Gate(nombre_puerta)

        # 3. Lo añadimos a la lista de puertas de esta área
        area.gates.append(nueva_puerta)

        # 4. MUY IMPORTANTE: Sumamos 1 al contador para que el while no sea infinito
        contador += 1