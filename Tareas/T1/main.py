import tablero
import dccasillas
import os

usuario = None
while not usuario:
      usuario = input("Ingrese su nombre de usuario: ").strip()
      if not usuario:
            print("El nombre de usuario no puede estar vacío. Inténtelo de nuevo.")

archivo_temporal = ""

while archivo_temporal == "":
      configuracion_tablero = str(input("Ingrese la configuración del tablero (nombre del archivo con el .txt): ")).strip()

      #revisar si el archivo existe https://stackoverflow.com/questions/2259382/pythonic-way-to-check-if-a-file-exists

      ruta = os.path.join("config", configuracion_tablero)

      if os.path.isfile(ruta):
            archivo_temporal = configuracion_tablero
      else:
            print("El archivo no existe. Por favor, verifique el nombre del archivo e intente nuevamente")
            
            
      

import_dccasillas = dccasillas.DCCasillas(usuario, archivo_temporal)
puntaje = 0
tableros_resueltos = 0
tableros_totales = import_dccasillas.total_tableros

import_tablero = tablero.Tablero()

def menu_juego():
    condicion = True
    if condicion == False:
            return

    while condicion:
      print(f"""
    ¡Bienvenido a DCCasillas! 
    Usuario: {usuario}, Puntaje: {puntaje} 
    Numero de tableros resueltos: {tableros_resueltos}/{tableros_totales}
    *** Menú de juego ***
    [1] Iniciar nuevo juego
    [2] Continuar juego
    [3] Guardar estado de juego
    [4] Recuperar estado de juego
    [5] Salir del programa
    """)
    

      accion = input("Indique su opción (1, 2, 3, 4, 5): ").strip()
    
      if accion == "1":
            if not import_dccasillas.tableros:
                  print("no hay tableros para jugar :c")
                  continue
            else:
                 import_dccasillas.tablero_actual = 0
                 tablero_juego = import_dccasillas.tableros[0]
                 tablero_juego.mostrar_tablero()
                 menu_acciones()
      elif accion == "2":
            if import_dccasillas.tablero_actual is not None:
                  tablero_juego = import_dccasillas.tableros[import_dccasillas.tablero_actual]
                  tablero_juego.mostrar_tablero()
                  menu_acciones()
            else:
                  print("No hay un tablero abierto para continuar.")
                  continue
      elif accion == "3":
            if import_dccasillas.guardar_estado():
                  print("Estado del juego guardado correctamente.")
                  continue
            else:
                  print("Error al guardar el estado del juego.")
                  continue
      elif accion == "4":
            if import_dccasillas.recuperar_estado():
                  print("Estado del juego recuperado correctamente.")
                  continue
            else:
                  print("Error al recuperar el estado del juego.")
                  continue
      elif accion == "5":
            print("Saliendo del programa...")
            condicion = False

def menu_acciones():
      condicion_2 = True
      if condicion_2 == False:
            return
      
      while condicion_2:     
            print(f"""
            *** Menú de Acciones ***
            [1] Mostrar tablero
            [2] Habilitar/deshabilitar casillas
            [3] Verificar solución
            [4] Encontrar solución
            [5] Volver al menú de Juego
            """)
            accion = input("Indique su opción (1, 2, 3, 4, 5): ").strip()

            if accion == "1":
                  tablero_juego = import_dccasillas.tableros[0]
                  tablero_juego.mostrar_tablero()

            elif accion not in ["1", "2", "3", "4", "5"]:
                  print("Utiliza un numero entre 1 y 5 plis")
                  accion = input("Indique su opción (1, 2, 3, 4, 5): ").strip()
                  continue

            elif accion == "2":
                  fila = input("Ingrese la fila de la casilla a modificar: ").strip()
                  columna = input("Ingrese la columna de la casilla a modificar: ").strip()
                  if fila.isdigit() and columna.isdigit():
                        fila = int(fila)
                        columna = int(columna)
                        if import_tablero.modificar_casilla(fila, columna):
                              print("Casilla modificada correctamente !!")
                        else:
                              print("Este movimiento no es valido >:(")
                  else:
                        print("Por favor, ingrese números válidos para fila y columna.")
            elif accion == "3":
                  if import_tablero.validar():
                       print("El tablero está solucionado!! :))")
                  else:
                        print("El tablero no está solucionado :(")
                 
            elif accion == "4":
                  solucion = import_tablero.encontrar_solucion()
                  if solucion:
                        print("Solución encontrada:")
                        solucion.mostrar_tablero()
                  else:
                        print("No se encontró una solución, intentalo de nuevo jeje")

            elif accion == "5":
                  print("Volviendo al menú de juego...")
                  condicion_2 = False
                  
menu_juego()