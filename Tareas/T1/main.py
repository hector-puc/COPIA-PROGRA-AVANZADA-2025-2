import tablero
import dccasillas
import os


nombre = input("Ingrese su nombre de usuario: ")
configuracion_tablero = input("Ingrese la configuración del tablero (nombre del archivo con el .txt): ")

#revisar si el archivo existe https://stackoverflow.com/questions/2259382/pythonic-way-to-check-if-a-file-exists

ruta = os.path.join("config", configuracion_tablero)

#if os.path.exists(ruta):
    

puntaje = 0
tableros_resueltos = 0
tableros_totales = dccasillas.total_tableros

print(f"""
      ¡Bienvenido a DCCasillas! 
      Usuario: {nombre}, Puntaje: {puntaje} 
      *** Menú de juego ***
      [1] Iniciar nuevo juego
      [2] Continuar juego
      [3] Guardar estado de juego
      [4] Recuperar estado de juego
      [5] Salir del programa

      Indique su opcion! :) (1, 2, 3, 4 o 5)
      """)
