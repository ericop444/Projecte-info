import os
from airport import *


def ejecutar_pruebas():
    print("PRUEBAS \n")

    # PRUEBA: IsSchengenAirport
    print("1. Probando IsSchengenAirport...")
    if IsSchengenAirport("LEBL") == True and IsSchengenAirport("EGLL") == False:
        print("Detecta bien Schengen (LEBL) y No Schengen (EGLL).")
    else:
        print(" ERROR en IsSchengenAirport.")

    # PRUEBA: Creación de clase y SetSchengen
    print("\n2. Probando clase Airport y SetSchengen...")
    a1 = Airport("LEBL", 41.29, 2.08)
    SetSchengen(a1)
    if a1.isSchengen == True:
        print(" El aeropuerto se creó y se actualizó a Schengen correctamente.")
    else:
        print("ERROR en SetSchengen o al crear el objeto.")

    # PRUEBA: AddAirport y RemoveAirport
    print("\n3. Probando AddAirport y RemoveAirport...")
    lista_prueba = []

    res_add = AddAirport(lista_prueba, a1)
    res_add_dup = AddAirport(lista_prueba, a1)  # Intentamos añadirlo otra vez
    if res_add == 0 and res_add_dup == -1 and len(lista_prueba) == 1:
        print(" AddAirport añade bien y bloquea duplicados (-1).")
    else:
        print(" ERROR en AddAirport.")

    res_rm = RemoveAirport(lista_prueba, "LEBL")
    res_rm_notfound = RemoveAirport(lista_prueba, "LEBL")  # Intentamos borrarlo cuando ya no está
    if res_rm == 0 and res_rm_notfound == -1 and len(lista_prueba) == 0:
        print(" RemoveAirport borra bien y avisa si no existe (-1).")
    else:
        print("  ERROR en RemoveAirport.")

    # PRUEBA: Carga y Guardado de archivos
    print("\n4. Probando LoadAirports y SaveSchengenAirports...")
    # Creamos un archivo de texto temporal solo para la prueba
    with open("test_input.txt", "w") as f:
        f.write("CODE LAT LON\n")
        f.write("LEBL N411749 E0020442\n")  # España (Schengen)
        f.write("EGLL N512839 W0002741\n")  # UK (No Schengen)

    lista_cargada = LoadAirports("test_input.txt")
    if len(lista_cargada) == 2:
        print("LoadAirports leyó el archivo bien.")

        for a in lista_cargada:
            SetSchengen(a)

        res_save = SaveSchengenAirports(lista_cargada, "test_output.txt")
        if res_save == 0 and os.path.exists("test_output.txt"):
            print(" SaveSchengenAirports guardó el archivo correctamente.")
        else:
            print(" ERROR en SaveSchengenAirports.")
    else:
        print(" ERROR en LoadAirports.")

    # Limpiamos los archivos temporales para no ensuciar la carpeta
    if os.path.exists("test_input.txt"): os.remove("test_input.txt")
    if os.path.exists("test_output.txt"): os.remove("test_output.txt")

    print("\n ¡COMPROBACIÓN  TERMINADA! ")



if __name__ == "__main__":
    ejecutar_pruebas()