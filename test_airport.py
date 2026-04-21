# Importamos todo desde tu archivo principal
from airport import *


def main():
    print("--- INICIANDO PRUEBA DEL PASO 5 ---")

    # 1. Cargamos los aeropuertos desde el archivo de texto
    archivo_entrada = "airports.txt"
    lista_aeropuertos = LoadAirports(archivo_entrada)

    if len(lista_aeropuertos) == 0:
        print("Error: No se ha podido cargar ningún aeropuerto. Revisa airports.txt")
        return

    print(f"Se han cargado {len(lista_aeropuertos)} aeropuertos correctamente.")

    # 2. Actualizamos el estado Schengen de cada aeropuerto
    # (Si no hacemos esto, todos saldrán como "No Schengen" por defecto)
    for aeropuerto in lista_aeropuertos:
        SetSchengen(aeropuerto)

    print("Estado Schengen calculado.")

    # 3. Llamamos a tu función para dibujar el gráfico
    print("Abriendo el gráfico... (Cierra la ventana del gráfico para terminar el programa)")
    PlotAirports(lista_aeropuertos)

    print("¡Prueba terminada con éxito!")


# Esto ejecuta la función main()
if __name__ == "__main__":
    main()