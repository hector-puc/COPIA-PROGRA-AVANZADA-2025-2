import sys
from parametros import ORO_POR_RONDA, ORO_POR_VICTORIA  
from funciones.leer_archivos import cargar_ias
from menus import cargar_cargas_archivo, catalogo_sin_repetir_nombres, construir_carta_desde_fila, tienda_menu, mover_del_mazo_a_coleccion
from funciones.jugador import Jugador
from funciones.ia import IA
from funciones import contexto


def mostrar_cartas_jugador(jugador):
    print("\nEstado actual:")
    print(f"Jugador - {jugador.nombre_jugador}| Tienes: {jugador.oro_disponible}G")
    print(f"Cartas en colección:")
    indice = 0
    
    while indice < len(jugador.coleccion):
        carta = jugador.coleccion[indice]
        print(f"{carta.nombre_carta} \ {carta.tipo_carta} | Vida: {carta.vida_actual}/{carta.vida_maxima}")
        indice += 1
    
    j = 0
    while j < len(jugador.mazo):
        indice_2 = jugador.mazo[j]
        print(f"({j+1}) {indice_2.nombre_carta}")
        j += 1
    print("-------------------\n")

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


def seleccion_inicial_mazo(instancia_jugador): #decidi que la seleccion sea igual de 4 cartas como clash
    print("\n=== SELECCIÓN INICIAL (elige 4) ===")
    cartas_pool = cargar_cargas_archivo()  

    while len(instancia_jugador.mazo) < 4:
        nombres_que_tiene = []
        #nombres que ya tiene para evitar duplicados
        for i in instancia_jugador.coleccion:
            nombres_que_tiene.append(i.nombre_carta)
        #catalogo aleatorio sin repetidos
        sugerencias = catalogo_sin_repetir_nombres(cartas_pool, nombres_que_tiene)

        if not sugerencias:
            print("No quedan cartas disponibles, las tienes todas")
            break

        print("Cartas sugeridas:")
        indice = 0
        while indice < len(sugerencias):
            carta = sugerencias[indice]
            print(f"[{indice+1}]. {carta.nombre_carta} ({carta.tipo_carta}) "
                  f"HP {carta.vida_actual}/{carta.vida_maxima}")
            indice += 1

        eleccion = input(f"Elige 1 sugerencia {len(sugerencias)} (tienes para elegir {4 - len(instancia_jugador.mazo)}) mas o 0 para refrescar: ").strip()
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
        instancia_jugador.coleccion.append(carta_elegida)
        instancia_jugador.mazo.append(carta_elegida)
        print(f"Agregada: {carta_elegida.nombre_carta}")

    print("Primeras cartas elegidas, bien hecho :DD")

def menu_inventario(instancia_jugador):
    #mueve cartas entre coleccion y mazo quita del mazo reordena el mazo

    while True:
        print ("INVENTARIO")
        print("1. Pasar de Colección a Mazo")
        print("2. Pasar de Mazo a Colección")
        print("3. Reordenar Mazo")
        print("0. Volver")
        opcion = input("> ").strip()

        if opcion == "0":
            return

        elif opcion == "1":
            mostrar_cartas_jugador(instancia_jugador)
            indice = input("Numero en coleccion a mover (0 para cancelar): ").strip()
            if not indice.isdigit():
                print("Elige bien 😡")
                continue
            indice = int(indice)
            if indice == 0:
                continue
            if indice < 1 or indice > len(instancia_jugador.coleccion):
                print("Elige bien 😡")
                continue
            if len(instancia_jugador.mazo) >= 5:
                print("El mazo ya tiene 5 cartas.")
                continue
            candidato = instancia_jugador.coleccion[indice - 1]
            for i in instancia_jugador.mazo:
                if i.nombre_carta == candidato.nombre_carta:
                    print("No puedes tener la misma carta")
                    continue
            instancia_jugador.mazo.append(candidato)
            print(f"Agregaste al mazo a: {candidato.nombre_carta}")

        elif opcion == "2":
            if not instancia_jugador.mazo:
                print("No tienes cartas en el mazo.")
                continue
            mostrar_cartas_jugador(instancia_jugador)
            indice = input("Numero de la carta que quieres quitar (0 para cancelar): ").strip()
            if not indice.isdigit():
                print("Elige bien 😡")
                continue
            indice = int(indice)
            if indice == 0:
                continue
            if indice < 1 or indice > len(instancia_jugador.mazo):
                print("Elige bien 😡")
                continue
            quitada = instancia_jugador.mazo.pop(indice - 1)
            print(f"Eliminaste del mazo a: {quitada.nombre_carta}\n")
            mover_del_mazo_a_coleccion(instancia_jugador, quitada)

        #para reordenar el mazo lo que pense fue que el usuario lo elija, es decir, que elija la posicion desde donde
        #quiere mover la carta y la posicion a donde quiere moverla (comenzando desde la posicion 1)
        elif opcion == "3":
            if len(instancia_jugador.mazo) < 2:
                print("Necesitas al menos 2 cartas para reordenar")
                continue
            mostrar_cartas_jugador(instancia_jugador)
            origen = input("Posición de la carta que quieres reordenar: ").strip()
            destino = input("Posición del destino donde quieres mover la carta: ").strip()
            if not origen.isdigit() or not destino.isdigit():
                print("Elige bien 😡")
                continue
            origen = int(origen) - 1
            destino = int(destino) - 1
            if origen < 0 or origen >= len(instancia_jugador.mazo) or destino < 0 or destino >= len(instancia_jugador.mazo):
                print("Elige bien 😡")
                continue
            carta = instancia_jugador.mazo.pop(origen)
            instancia_jugador.mazo.insert(destino, carta)
            print("Reordenado! :D")

        else:
            print("Elige bien 😡")

#combate (al fin)

def ejecutar_una_ronda(instancia_jugador, lista_ias, indice_ia_actual):
    if indice_ia_actual >= len(lista_ias):
        print("No quedan IAs! Ganaste el juego :)")
        return indice_ia_actual

    ia = lista_ias[indice_ia_actual]

    if not instancia_jugador.mazo:
        print("Tu mazo está vacio. Busca en tu inventario o tienda")
        return indice_ia_actual

    print(f"\n=== COMIENZA LA RONDA CONTRA {ia.nombre}")
    contexto.ejecutar_ronda_ccontexto(instancia_jugador, ia, instancia_jugador.mazo)

    instancia_jugador.oro_disponible += ORO_POR_RONDA
    if getattr(ia, "vida", ia.vida_maxima) <= 0:
        instancia_jugador.oro_disponible += ORO_POR_VICTORIA
        print(f"Derrotaste a {ia.nombre}!. Eres un crack! +{ORO_POR_VICTORIA}G")
        indice_ia_actual += 1

    return indice_ia_actual

#menu
def menu_principal(instancia_jugador, lista_ias):
    indice_ia_actual = 0
    mismo_catalogo = None 

    while True:
        print("MENÚ PRINCIPAL:")
        print("1. Ver información de mis cartas")
        print("2. Inventario")
        print("3. Tienda")
        print("4. Entrar en combate")
        print("0. Salir")
        opcion = input("> ").strip()

        #veotodo del enunciado (en caso de hacer la wea)
        
        
        if opcion == "0":
            print("Hasta luego !")
            break

        elif opcion == "1":
            mostrar_cartas_jugador(instancia_jugador)

        elif opcion == "2":
            menu_inventario(instancia_jugador)

        elif opcion == "3":
            mismo_catalogo = tienda_menu(instancia_jugador, mismo_catalogo)

        elif opcion == "4":
            ia = lista_ias[indice_ia_actual]
            while ia.vida > 0 and instancia_jugador.hay_alguna_carta_viva():
                indice_ia_actual = ejecutar_una_ronda(instancia_jugador, lista_ias, indice_ia_actual)

        else:
            print("Elige bien 😡")

# inicio
def principio():
    if len(sys.argv) < 3:
        print("Uso: python3 main.py <facil|normal|dificil | archivo_guardado> <nombre_jugador>")
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
