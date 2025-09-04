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

if __name__ == "__main__":
    principio()

