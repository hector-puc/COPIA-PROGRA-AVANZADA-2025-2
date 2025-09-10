from random import sample, randint
from funciones.leer_archivos import cargar_cartas
from funciones.tropa import Tropa
from funciones.estructura import Estructura
from funciones.mixta import Mixta
from parametros import (COSTO_REROLL, COSTO_CURAR, COSTO_REVIVIR, COSTO_COMBINACION, )

#convierte una fila de cargar_cartas() a una tropa o estructura
def construir_carta_desde_fila(fila_de_cartas):
    
    nombre_carta_desde_archivo = str(fila_de_cartas["nombre"]).strip()
    tipo_carta_desde_archivo = str(fila_de_cartas["tipo"]).strip().lower()
    vida_maxima_desde_archivo = int(fila_de_cartas["vida_maxima"])  # vida_actual parte igual a vida_maxima
    multiplicador_defensa_desde_archivo = float(fila_de_cartas["multiplicador_defensa"])
    precio_carta_desde_archivo = int(fila_de_cartas["precio"]) 
    probabilidad_especial_desde_archivo = float(fila_de_cartas["probabilidad_especial"])  


    if tipo_carta_desde_archivo == "tropa":
        ataque_base_desde_archivo = int(fila_de_cartas["ataque"])
        multiplicador_ataque_desde_archivo = float(fila_de_cartas["multiplicador_ataque"])
        descripcion_habilidad_desde_archivo = str(fila_de_cartas["descripcion_habilidad"])
        instancia_carta = Tropa(nombre_carta = nombre_carta_desde_archivo, tipo_carta = "tropa", vida_maxima = vida_maxima_desde_archivo, multiplicador_defensa = multiplicador_defensa_desde_archivo, precio_carta = precio_carta_desde_archivo, probabilidad_especial = probabilidad_especial_desde_archivo, ataque_base = ataque_base_desde_archivo, multiplicador_ataque = multiplicador_ataque_desde_archivo, habilidad_especial = descripcion_habilidad_desde_archivo)
        return instancia_carta

    else:
        ataque_base_desde_archivo = 0
        multiplicador_ataque_desde_archivo = 0.0
        descripcion_habilidad_desde_archivo = str(fila_de_cartas["descripcion_habilidad"])

        instancia_carta = Estructura(nombre_carta = nombre_carta_desde_archivo, tipo_carta = "estructura", vida_maxima = vida_maxima_desde_archivo, multiplicador_defensa = multiplicador_defensa_desde_archivo, precio_carta = precio_carta_desde_archivo, probabilidad_especial = probabilidad_especial_desde_archivo, ataque_base = ataque_base_desde_archivo, multiplicador_ataque = multiplicador_ataque_desde_archivo, habilidad_especial = descripcion_habilidad_desde_archivo )
        return instancia_carta

# catalogo cartas

def cargar_cargas_archivo():
    return cargar_cartas()

#decidi que no se puedan repetir cartas que ya se tengan y que sea aleatorio el tamaño del mazo
def catalogo_sin_repetir_nombres(cartas, cartas_jugador):
    filas_posibles = []
    indice_busqueda = 0
    while indice_busqueda < len(cartas):
        fila_actual = cartas[indice_busqueda]
        nombre_en_fila = str(fila_actual["nombre"]).strip()
        if nombre_en_fila not in cartas_jugador:
            filas_posibles.append(fila_actual)
        indice_busqueda += 1

    if len(filas_posibles) == 0:
        return []

    cantidad_mininma = 3
    cantidas_maxima = 5

    cantidad_final = cantidad_mininma
    if len(filas_posibles) > cantidad_mininma: #debug
        limite_maximo = cantidas_maxima
        if len(filas_posibles) < cantidas_maxima:
            limite_maximo = len(filas_posibles)
        cantidad_final = randint(cantidad_mininma, limite_maximo)

    filas_elegidas = sample(filas_posibles, cantidad_final)

    lista_catalogo = []
    indice_construccion = 0
    while indice_construccion < len(filas_elegidas):
        instancia_construida = construir_carta_desde_fila(filas_elegidas[indice_construccion])
        lista_catalogo.append(instancia_construida)
        indice_construccion += 1

    return lista_catalogo


def mostrar_catalogo(cartas_catalogo):
    print("TIENDA")
    print("-----------------------------")
    print("Cartas disponibles:")

    indice = 0
    while indice < len(cartas_catalogo):
        carta_actual = cartas_catalogo[indice]
        numero_opcion = indice + 1
        print(f"[{numero_opcion}] {carta_actual.nombre_carta} ---- {carta_actual.precio_carta}G")
        indice += 1

#tienda

def comprar_carta(instancia_jugador, cartas_catalogo, numero_de_opcion_humano):
    indice_real_en_lista = numero_de_opcion_humano - 1
    if indice_real_en_lista < 0 or indice_real_en_lista >= len(cartas_catalogo):
        print("Elige bien 😡")
        return False

    carta_para_comprar = cartas_catalogo[indice_real_en_lista]

    # verificar que no la tenga ya en su coleccion
    nombres_cartas_coleccion = []
    indice_recorre_coleccion = 0
    while indice_recorre_coleccion < len(instancia_jugador.coleccion):
        nombres_cartas_coleccion.append(instancia_jugador.coleccion[indice_recorre_coleccion].nombre_carta)
        indice_recorre_coleccion += 1

    if carta_para_comprar.nombre_carta in nombres_cartas_coleccion:
        print("Ya tienes esa carta :p")
        return False

    if instancia_jugador.oro_disponible < carta_para_comprar.precio_carta:
        print("Eres pobre y no tienes oro jejeje")
        return False

    instancia_jugador.oro_disponible -= carta_para_comprar.precio_carta
    instancia_jugador.coleccion.append(carta_para_comprar)
    print(f"Compraste {carta_para_comprar.nombre_carta} por {carta_para_comprar.precio_carta}G.")
    return True


def curar_cartas(instancia_jugador):
    cartas_heridas = []
    indice = 0
    while indice < len(instancia_jugador.coleccion):
        temporal = instancia_jugador.coleccion[indice]
        if temporal.vida_actual > 0 and temporal.vida_actual < temporal.vida_maxima:
            cartas_heridas.append(temporal)
        indice += 1

    if len(cartas_heridas) == 0:
        print("No tienes cartas que curar (god).")
        return False

    if instancia_jugador.oro_disponible < COSTO_CURAR:
        print("No tienes oro :pp")
        return False

    print("Cartas con daño:")
    indice_muestra = 0
    while indice_muestra < len(cartas_heridas):
        carta_danada = cartas_heridas[indice_muestra]
        print(f"[{indice_muestra+1}] {carta_danada.nombre_carta} {carta_danada.vida_actual}/{carta_danada.vida_maxima} HP")
        indice_muestra += 1

    carta_a_curar = input(f"Elige carta a curar (costo {COSTO_CURAR}G) o 0 para volver: ").strip()
    if not carta_a_curar.isdigit():
        print("Elige bien 😡")
        return False

    numero_elegido = int(carta_a_curar)
    if numero_elegido == 0:
        print("Volviendo al menu...")
        print("----------------")
        return False
    if numero_elegido < 1 or numero_elegido > len(cartas_heridas):
        print("Elige bien 😡")
        return False

    carta_elegida = cartas_heridas[numero_elegido - 1]

    instancia_jugador.oro_disponible -= COSTO_CURAR
    carta_elegida.vida_actual = carta_elegida.vida_maxima
    print(f"Has curado a {carta_elegida.nombre_carta}")
    return True


def revivir_carta(instancia_jugador):
    lista_de_cartas_muertas = []
    indice = 0
    while indice < len(instancia_jugador.coleccion):
        temporal = instancia_jugador.coleccion[indice]
        if temporal.vida_actual == 0:
            lista_de_cartas_muertas.append(temporal)
        indice += 1

    if len(lista_de_cartas_muertas) == 0:
        print("No tienes cartas en el lobby :D")
        return False

    print("Cartas en el lobby:")
    indice_muestra = 0
    while indice_muestra < len(lista_de_cartas_muertas):
        carta_muerta = lista_de_cartas_muertas[indice_muestra]
        costo_revivir_individual = int(round(carta_muerta.precio_carta * COSTO_REVIVIR))
        print(f"[{indice_muestra+1}] {carta_muerta.nombre_carta} (revivir: {costo_revivir_individual}G)")
        indice_muestra += 1

    entrada_usuario_revivir = input("Elige carta a revivir o 0 para volver: ").strip()
    if not entrada_usuario_revivir.isdigit():
        print("Elige bien 😡")
        return False

    numero_elegido = int(entrada_usuario_revivir)

    if numero_elegido == 0:
        print("Volviendo al menú...")
        print("----------------")
        return False
    if numero_elegido < 1 or numero_elegido > len(lista_de_cartas_muertas):
        print("Elige bien 😡")
        return False

    carta_para_revivir = lista_de_cartas_muertas[numero_elegido - 1]
    costo_revivir = int(round(carta_para_revivir.precio_carta * COSTO_REVIVIR))

    if instancia_jugador.oro_disponible < costo_revivir:
        print("no tienes oro suficiente")
        return False

    instancia_jugador.oro_disponible -= costo_revivir
    carta_para_revivir.vida_actual = carta_para_revivir.vida_maxima
    print(f"{carta_para_revivir.nombre_carta} ha sido revivida.")
    return True


def taller_combinar(instancia_jugador):
    lista_tropas = []
    lista_estructuras = []

    indice = 0
    while indice < len(instancia_jugador.coleccion):
        temporal = instancia_jugador.coleccion[indice]
        if temporal.tipo_carta == "tropa":
            lista_tropas.append(temporal)
        elif temporal.tipo_carta == "estructura":
            lista_estructuras.append(temporal)
        indice += 1

    if len(lista_tropas) == 0 or len(lista_estructuras) == 0:
        print("Necesitas por lo menos una tropa y una estructura para combinar")
        return False

    if instancia_jugador.oro_disponible < COSTO_COMBINACION:
        print("No tienes oro suficiente para combinar :pp")
        return False

    print("Tropas disponibles:")
    indice_muestra = 0
    while indice_muestra < len(lista_tropas):
        tropa_actual = lista_tropas[indice_muestra]
        print(f"[{indice_muestra+1}] {tropa_actual.nombre_carta}")
        indice_muestra += 1

    entrada_usuario_tropa = input("Elige la tropa (número) o 0 para volver: ").strip()
    if not entrada_usuario_tropa.isdigit():
        print("Elige bien 😡")
        return False

    numero_tropa_elegida = int(entrada_usuario_tropa)
    if numero_tropa_elegida == 0:
        print("Volviendo al menu...")
        print("----------------")
        return False
    if numero_tropa_elegida < 1 or numero_tropa_elegida > len(lista_tropas):
        print("Elige bien 😡")
        return False

    print("Estructuras disponibles:")
    indice_muestra = 0
    while indice_muestra < len(lista_estructuras):
        estructura_actual = lista_estructuras[indice_muestra]
        print(f"[{indice_muestra+1}] {estructura_actual.nombre_carta}")
        indice_muestra += 1

    estructura_numero = input("Elige la estructura o 0 para volver: ").strip()
    if not estructura_numero.isdigit():
        print("Elige bien 😡")
        return False

    estructura_numero = int(estructura_numero)
    if estructura_numero == 0:
        return False
    if estructura_numero < 1 or estructura_numero > len(lista_estructuras):
        print("Elige bien 😡")
        return False

    tropa_seleccionada = lista_tropas[numero_tropa_elegida - 1]
    estructura_seleccionada = lista_estructuras[estructura_numero - 1]

    instancia_jugador.oro_disponible -= COSTO_COMBINACION
    carta_mixta_creada = Mixta(tropa_seleccionada, estructura_seleccionada)

    # eliminar del mazo y de la coleccion 
    indice_mazo = 0
    while indice_mazo < len(instancia_jugador.mazo):
        carta_mazo = instancia_jugador.mazo[indice_mazo]
        if carta_mazo is tropa_seleccionada or carta_mazo is estructura_seleccionada:
            instancia_jugador.mazo.pop(indice_mazo)
            indice_mazo -= 1
        indice_mazo += 1

    indice_coleccion = 0
    while indice_coleccion < len(instancia_jugador.coleccion):
        carta_en_coleccion = instancia_jugador.coleccion[indice_coleccion]
        if carta_en_coleccion is tropa_seleccionada or carta_en_coleccion is estructura_seleccionada:
            instancia_jugador.coleccion.pop(indice_coleccion)
            indice_coleccion -= 1
        indice_coleccion += 1

    instancia_jugador.coleccion.append(carta_mixta_creada)
    print(f"Has creado {carta_mixta_creada.nombre_carta} pagando {COSTO_COMBINACION}G.")
    return True

#menu tienda

def tienda_menu(instancia_jugador, lista_catalogo = None):
    
    #mantiene el catalogo hasta que se haga reroll
    
    cartas = cargar_cargas_archivo()

    if lista_catalogo is None or len(lista_catalogo) == 0:
        lista_que_se_tienen = []
        indice = 0
        while indice < len(instancia_jugador.coleccion):
            lista_que_se_tienen.append(instancia_jugador.coleccion[indice].nombre_carta)
            indice += 1
        lista_catalogo = catalogo_sin_repetir_nombres(cartas, lista_que_se_tienen)

    while True:
        print("----------------------")
        print("TIENDA")
        print("----------------------")
        print(f"Dinero disponible: {instancia_jugador.oro_disponible}G")

        mostrar_catalogo(lista_catalogo)

        cantidad_de_opciones_de_compra = len(lista_catalogo)
        print(f"[{cantidad_de_opciones_de_compra + 1}] Curar carta")
        print(f"[{cantidad_de_opciones_de_compra + 2}] Revivir carta")
        print(f"[{cantidad_de_opciones_de_compra + 3}] Reroll (costo {COSTO_REROLL}G)")
        print(f"[{cantidad_de_opciones_de_compra + 4}] Taller (combinar cartas)")
        print("[0] Volver al Menú principal")
        opcion = input("Indique su opción: ").strip()
        if not opcion.isdigit():
            print("Elige bien 😡")
            continue

        numero_opcion = int(opcion)
        if numero_opcion == 0:
            return lista_catalogo

        #comprar
        if 1 <= numero_opcion <= cantidad_de_opciones_de_compra:
            compra_exitosa = comprar_carta(instancia_jugador, lista_catalogo, numero_opcion)
            if compra_exitosa:
                #quitar de la lista
                lista_catalogo.pop(numero_opcion - 1)
            continue

        #curar
        if numero_opcion == cantidad_de_opciones_de_compra + 1:
            curar_cartas(instancia_jugador)
            continue

        #revivir
        if numero_opcion == cantidad_de_opciones_de_compra + 2:
            revivir_carta(instancia_jugador)
            continue

        #reroll
        if numero_opcion == cantidad_de_opciones_de_compra + 3:
            if instancia_jugador.oro_disponible < COSTO_REROLL:
                print("No tienes oro suficiente D:")
                continue
            instancia_jugador.oro_disponible -= COSTO_REROLL

            lista_que_se_tienen = []
            indice = 0
            while indice < len(instancia_jugador.coleccion):
                lista_que_se_tienen.append(instancia_jugador.coleccion[indice].nombre_carta)
                indice += 1

            lista_catalogo = catalogo_sin_repetir_nombres(cartas, lista_que_se_tienen)
            print("Reroll hecho ! :)")
            continue

        #taller
        if numero_opcion == cantidad_de_opciones_de_compra + 4:
            taller_combinar(instancia_jugador)
            continue

        print("Elige bien 😡")
