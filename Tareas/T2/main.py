import sys
from funciones.leer_archivos import cargar_cartas, cargar_ias, cargar_multiplicadores
import funciones.ia

def principio():
    if len(sys.argv) < 3:
        print("Tienes que elegir dificultad y el nombre de usuario al momento de ejecutar el codigo! :)")
        return

    argumento_1 = sys.argv[1]
    
    if argumento_1 in ["facil", "normal", "dificil"]:
        dificultad = argumento_1
        nombre = sys.argv[2]

        lista_multiplicadores = cargar_multiplicadores()
        ias_nombre = cargar_ias(dificultad)

        funciones.ia.cargar_multiplicadores() ######## 
        
        print(f"Iniciando partida en dificultad {dificultad}...")

    else:
        archivo = sys.argv[1]

        print("Iniciando archivo de guardado...")

if __name__ == "__main__": # para saber si se ejecuta desde la terminal el archivo main.py
    principio()

