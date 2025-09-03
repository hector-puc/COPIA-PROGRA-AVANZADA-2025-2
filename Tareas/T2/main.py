import sys
from funciones.leer_archivos import cargar_cartas, cargar_ias, cargar_multiplicadores
def principio():
    if len(sys.argv) < 3:
        print("Tienes que elegir dificultad y el nombre de usuario al momento de ejecutar el codigo! :)")
        return

    argumento_1 = sys.argv[1]
    
    if argumento_1 in ["facil", "normal", "dificil"]:
        dificultad = argumento_1
        nombre = sys.argv[2]

        print(f"Iniciando partida en dificultad {dificultad}...")

    else:
        archivo = sys.argv[1]

        print("Iniciando archivo de guardado...")

    print("=== CARTAS ===")
    lista_de_cartas = cargar_cartas()
    print(f"Se cargaron {len(lista_de_cartas)} cartas.")
    for carta in lista_de_cartas[:3]:  # mostrar solo las 3 primeras
        print(carta)

    # Probar IAs en dificultad fácil
    print("\n=== IAs FACIL ===")
    dificultad = dificultad.strip()
    lista_de_ias = cargar_ias(dificultad)
    print(f"Se cargaron {len(lista_de_ias)} IAs (facil).")
    for ia in lista_de_ias:
        print(ia)

    # Probar multiplicadores
    print("\n=== MULTIPLICADORES ===")
    lista_de_multiplicadores = cargar_multiplicadores()
    print(f"Se cargaron {len(lista_de_multiplicadores)} multiplicadores.")
    for multiplicador in lista_de_multiplicadores[:3]:
        print(multiplicador)

if __name__ == "__main__":
    principio()

