
from airport import *

def main():
    # 1. Cargar los aeropuertos desde el archivo de texto
    archivo_entrada = "airports.txt"
    print(f"--- 1. Cargando aeropuertos desde {archivo_entrada} ---")
    lista_aeropuertos = LoadAirports(archivo_entrada)
    print(f"Se han cargado {len(lista_aeropuertos)} aeropuertos.\n")

    # 2. Actualizar el estado Schengen de todos los aeropuertos cargados
    print("--- 2. Actualizando el estado Schengen ---")
    for aeropuerto in lista_aeropuertos:
        SetSchengen(aeropuerto)
    print("Estado Schengen actualizado para todos los aeropuertos.\n")

    # 3. Probar a añadir un nuevo aeropuerto (Ej: Madrid Barajas - LEMD)
    print("--- 3. Añadiendo aeropuerto LEMD ---")
    nuevo_aeropuerto = Airport("LEMD", 40.493556, -3.566764)
    SetSchengen(nuevo_aeropuerto) # No olvidemos calcular si es Schengen

    if AddAirport(lista_aeropuertos, nuevo_aeropuerto) == 0:
        print("Aeropuerto LEMD añadido con éxito.\n")
    else:
        print("Error: El aeropuerto LEMD ya existía en la lista.\n")

    # 4. Probar a eliminar un aeropuerto (Ej: Reykjavik - BIKF)
    print("--- 4. Eliminando aeropuerto BIKF ---")
    if RemoveAirport(lista_aeropuertos, "BIKF") == 0:
        print("Aeropuerto BIKF eliminado con éxito.\n")
    else:
        print("Error: No se encontró el aeropuerto BIKF.\n")

    # 5. Guardar solo los aeropuertos Schengen en un archivo nuevo
    archivo_salida = "schengen.txt"
    print(f"--- 5. Guardando aeropuertos Schengen en {archivo_salida} ---")
    if SaveSchengenAirports(lista_aeropuertos, archivo_salida) == 0:
        print("Archivo guardado correctamente. ¡Revisa tu carpeta!")
    else:
        print("Error al guardar. La lista no tenía aeropuertos Schengen o estaba vacía.")

# Esto asegura que el código principal se ejecute cuando le des al Play
if __name__ == "__main__":
    main()
