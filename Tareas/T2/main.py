import sys
from parametros import ORO_POR_RONDA, ORO_POR_VICTORIA  
from funciones.leer_archivos import cargar_ias
from menus import cargar_cargas_archivo, catalogo_sin_repetir_nombres, construir_carta_desde_fila, tienda_menu, mover_del_mazo_a_coleccion, linea_carta_en_una_linea
from funciones.jugador import Jugador
from funciones.ia import IA
from funciones import contexto


def mostrar_cartas_jugador(jugador):
    print("\nEstado actual:")
    print(f"Jugador - {jugador.nombre_jugador}| Tienes: {jugador.oro_disponible}G")
    print("\nCartas en colección:\n")
    indice_mostrado = 1
    while indice_mostrado <= len(jugador.coleccion):
        carta_actual = jugador.coleccion[indice_mostrado - 1]
        print(f"({indice_mostrado}) {linea_carta_en_una_linea(carta_actual)}")
        indice_mostrado += 1

    print("\nCartas en tu mazo:\n")
    indice_mostrado = 1
    while indice_mostrado <= len(jugador.mazo):
        carta_actual = jugador.mazo[indice_mostrado - 1]
        print(f"({indice_mostrado}) {linea_carta_en_una_linea(carta_actual)}")
        indice_mostrado += 1


def crear_ias(dificultad):

    filas_ias = cargar_ias(dificultad) 
    lista_instancias = []

    indice = 0
    while indice < len(filas_ias):
        f = filas_ias[indice]
        nombre = str(f["nombre"])
        vida_maxima = int(f["vida_maxima"])
        ataque = int(f["ataque"])
        descripcion = str(f["descripcion"])
        probabilidad_especial = float(f["probabilidad_especial"])
        velocidad = float(f["velocidad"])

        ia = IA(nombre, vida_maxima, ataque, descripcion, probabilidad_especial, velocidad)
        ia.inyectar_multiplicadores() 
        lista_instancias.append(ia)
        indice += 1

    return lista_instancias


def seleccion_inicial_mazo(jugador): #decidi que la seleccion sea igual de 4 cartas como clash
    print("\n--- SELECCIÓN INICIAL (elige 4) ----\n")
    cartas_pool = cargar_cargas_archivo()  

    while len(jugador.mazo) < 4:
        nombres_que_tiene = []
        #nombres que ya tiene para evitar duplicados
        for i in jugador.coleccion:
            nombres_que_tiene.append(i.nombre_carta)
        #catalogo aleatorio sin repetidos
        sugerencias = catalogo_sin_repetir_nombres(cartas_pool, nombres_que_tiene)

        if not sugerencias:
            print("No quedan cartas disponibles, las tienes todas")
            break

        print("\nCartas sugeridas:\n")
        indice = 0
        while indice < len(sugerencias):
            carta = sugerencias[indice]
            print(f"[{indice+1}]. {carta.nombre_carta} ({carta.tipo_carta}) "
                  f"HP {carta.vida_actual}/{carta.vida_maxima}")
            indice += 1

        eleccion = input(f"\nElige 1 sugerencia {len(sugerencias)} (tienes para elegir {4 - len(jugador.mazo)}) mas o 0 para refrescar: \n").strip()
        if not eleccion.isdigit():
            print("Elige bien 😡")
            continue

        n = int(eleccion)
        if n == 0:
            #reroll
            continue
        if n < 1 or n > len(sugerencias):
            print("Elige bien 😡")
            continue

        carta_elegida = sugerencias[n - 1]
        #agrega a mazo y coleccion
        jugador.coleccion.append(carta_elegida)
        jugador.mazo.append(carta_elegida)
        print(f"Agregada: {carta_elegida.nombre_carta}")

    print("Primeras cartas elegidas, bien hecho :DD")

def menu_inventario(jugador):
    #mueve cartas entre coleccion y mazo quita del mazo reordena el mazo

    while True:
        print("\n------------------------")
        print("      INVENTARIO")
        print("------------------------")
        print("1. Pasar de Colección a Mazo")
        print("2. Pasar de Mazo a Colección")
        print("3. Reordenar Mazo")
        print("0. Volver")
        print("-------------------------------------\n")
        opcion = input("> ").strip()

        if opcion == "0":
            return

        elif opcion == "1":
            mostrar_cartas_jugador(jugador)
            indice = input("Numero en coleccion a mover (0 para cancelar): ").strip()
            if not indice.isdigit():
                print("Elige bien 😡")
                continue
            indice = int(indice)
            if indice == 0:
                continue
            if indice < 1 or indice > len(jugador.coleccion):
                print("Elige bien 😡")
                continue
            if len(jugador.mazo) >= 5:
                print("El mazo ya tiene 5 cartas.")
                continue
            candidato = jugador.coleccion[indice - 1]
            for i in jugador.mazo:
                if i.nombre_carta == candidato.nombre_carta:
                    print("No puedes tener la misma carta")
                    break
            jugador.mazo.append(candidato)
            print(f"Agregaste al mazo a: {candidato.nombre_carta}")
            jugador.coleccion.remove(candidato)
            

        elif opcion == "2":
            if not jugador.mazo:
                print("No tienes cartas en el mazo.")
                continue
            mostrar_cartas_jugador(jugador)
            indice = input("Numero de la carta que quieres quitar (0 para cancelar): ").strip()
            if not indice.isdigit():
                print("Elige bien 😡")
                continue
            indice = int(indice)
            if indice == 0:
                continue
            if indice < 1 or indice > len(jugador.mazo):
                print("Elige bien 😡")
                continue
            quitada = jugador.mazo.pop(indice - 1)
            print(f"Eliminaste del mazo a: {quitada.nombre_carta}\n")
            mover_del_mazo_a_coleccion(jugador, quitada)

        #para reordenar el mazo lo que pense fue que el usuario lo elija, es decir, que elija la posicion desde donde
        #quiere mover la carta y la posicion a donde quiere moverla (comenzando desde la posicion 1)
        elif opcion == "3":
            if len(jugador.mazo) < 2:
                print("Necesitas al menos 2 cartas para reordenar")
                continue
            mostrar_cartas_jugador(jugador)
            origen = input("Posición de la carta que quieres reordenar: ").strip()
            destino = input("Posición del destino donde quieres mover la carta: ").strip()
            if not origen.isdigit() or not destino.isdigit():
                print("Elige bien 😡")
                continue
            origen = int(origen) - 1
            destino = int(destino) - 1
            if origen < 0 or origen >= len(jugador.mazo) or destino < 0 or destino >= len(jugador.mazo):
                print("Elige bien 😡")
                continue
            carta = jugador.mazo.pop(origen)
            jugador.mazo.insert(destino, carta)
            print("Reordenado! :D")

        else:
            print("Elige bien 😡")

#combate (al fin)

def ejecutar_una_ronda(jugador, lista_ias, indice_ia_actual):
    if indice_ia_actual >= len(lista_ias):
        print("No quedan IAs! Ganaste el juego :)")
        return indice_ia_actual

    ia = lista_ias[indice_ia_actual]

    if not jugador.mazo:
        return indice_ia_actual

    print(f"\n--- COMIENZA LA RONDA CONTRA {ia.nombre} ----")
    print(f"Vida IA: {ia.vida}/{ia.vida_maxima}")

    contexto.ejecutar_ronda_ccontexto(jugador, ia, jugador.mazo)

    jugador.oro_disponible += ORO_POR_RONDA
    print(f"Terminó la ronda! +{ORO_POR_RONDA}G\n")
    if getattr(ia, "vida", ia.vida_maxima) <= 0:
        jugador.oro_disponible += ORO_POR_VICTORIA
        print(f"Derrotaste a {ia.nombre}!. Eres un crack! +{ORO_POR_VICTORIA}G\n")
        indice_ia_actual += 1

    return indice_ia_actual

#menu
def menu_principal(jugador, lista_ias):
    indice_ia_actual = 0
    mismo_catalogo = None 

    while True:
        
        print("\n---------------------------------")
        print("         MENÚ PRINCIPAL:         ")
        print("---------------------------------\n")
        print("1. Ver información de mis cartas")
        print("2. Inventario")
        print("3. Tienda")
        print("4. Entrar en combate")
        print("5. Espiar a la IA")
        print("0. Salir\n")
        opcion = input("> ").strip()

        #veotodo del enunciado (en caso de hacer la wea)
        
        
        if opcion == "0":
            print("Hasta luego !")
            break

        elif opcion == "1":
            mostrar_cartas_jugador(jugador)

        elif opcion == "2":
            menu_inventario(jugador)

        elif opcion == "3":
            mismo_catalogo = tienda_menu(jugador, mismo_catalogo)

        elif opcion == "4":
            
            ia = lista_ias[indice_ia_actual]    
            indice_ia_actual = ejecutar_una_ronda(jugador, lista_ias, indice_ia_actual)

            if not jugador.hay_alguna_carta_viva():
                print("No tienes cartas vivas en el mazo, perdiste ;(\n")
                print("\nSi quieres seguir ve a la tienda o taller :D")
                print("-----------------------------------------------")
        
        elif opcion == "5":
            ia = lista_ias[indice_ia_actual]
            print(f"\nIA Actual: {ia.nombre}")
            print(f"Vida: {ia.vida}/{ia.vida_maxima}")
            print(f"Descripción: {ia.descripcion}\n")
        else:
            print("Elige bien 😡")

# inicio
def principio():
    if len(sys.argv) < 3:
        print("Busca la forma correcta de ejecutar el programa")
        return

    argumento_1 = sys.argv[1].strip().lower()

    if argumento_1 in ("facil", "normal", "dificil"):
        dificultad = argumento_1
        nombre_jugador = sys.argv[2].strip()

        jugador = Jugador(nombre_jugador)

        #4 cartas iniciales
        seleccion_inicial_mazo(jugador)

        #contruir ia
        lista_ias = crear_ias(dificultad)

        print(f"Iniciando partida en dificultad {dificultad}...")
        menu_principal(jugador, lista_ias)


# para ver si se ejecuta el archivo correcto
#https://www.freecodecamp.org/espanol/news/python-if-name-main
if __name__ == "__main__":
    principio()
