from random import random
from funciones.contexto import Contexto

def cartas_vivas(mazo):
    vivas = []
    i = 0
    while i < len(mazo):
        carta = mazo[i]
        if carta.vida_actual > 0:
            vivas.append(carta)
        i += 1
    return vivas

def estructuras_y_mixtas_vivas(mazo):
    defensivas = []
    i = 0
    while i < len(mazo):
        carta = mazo[i]
        if (carta.tipo_carta == "estructura" or carta.tipo_carta == "mixta") and carta.vida_actual > 0:
            defensivas.append(carta)
        i += 1
    return defensivas

def tropas_vivas(mazo):
    tropas = []
    i = 0
    while i < len(mazo):
        carta = mazo[i]
        if carta.tipo_carta == "tropa" and carta.vida_actual > 0:
            tropas.append(carta)
        i += 1
    return tropas


def decidir_quien_ataca_primero(instancia_ia):
    velocidad_jugador = random()
    if instancia_ia.velocidad >= velocidad_jugador:
        return "ia"
    else:
        return "jugador"

def crear_contexto(instancia_jugador, instancia_ia, orden_ataca_primero):
    return Contexto(instancia_jugador = instancia_jugador, instancia_ia = instancia_ia, lista_cartas_aliadas = instancia_jugador.mazo, orden_ataca_primero = orden_ataca_primero, generador_aleatorio = random, registro_eventos = [])

def anotar(contexto, mensaje):
    contexto.registro_eventos.append(str(mensaje))


def inicio_de_ronda(contexto):
    #aca se revisa si hay montaptos
    vivas = cartas_vivas(contexto.instancia_jugador.mazo)
    i = 0
    while i < len(vivas):
        vivas[i].antes_de_ataque_del_jugador(contexto)
        i += 1

    #se agregan los buffs
    vivas = cartas_vivas(contexto.instancia_jugador.mazo)
    i = 0
    while i < len(vivas):
        vivas[i].inicio_de_ronda(contexto)
        i += 1

def fin_de_ronda(contexto):
    #se revierten los buffs
    vivas = cartas_vivas(contexto.instancia_jugador.mazo)
    i = 0
    while i < len(vivas):
        vivas[i].fin_de_ronda(contexto)
        i += 1

def ataque_jugador(contexto):
    jugador = contexto.instancia_jugador
    ia = contexto.instancia_ia

    vivas = cartas_vivas(jugador.mazo)
    i = 0
    while i < len(vivas) and ia.sigue_vivo():
        carta = vivas[i]
        carta.atacar(contexto)
        i += 1

def ataque_ia(contexto):
    jugador = contexto.instancia_jugador
    ia = contexto.instancia_ia

    #aqui se revisa si la ia tiene habilidad especial
    ia.usar_habilidad_especial(jugador)
    if not ia.sigue_vivo():
        return

    dano_total_ia = int(ia.ataque)
    if dano_total_ia <= 0:
        return

    multiplicadr_tropa = float(ia.multiplicadores_ataque["tropa"])
    multiplicador_estructura = float(ia.multiplicadores_ataque["estructura"])
    multiplicador_tropa = float(ia.multiplicadores_ataque["mixta"])

    jugador.recibir_dano_de_ia(dano_total_ia, multiplicadr_tropa, multiplicador_estructura, multiplicador_tropa, contexto)


def ejecutar_ronda(instancia_jugador, instancia_ia):
    orden_inicial = decidir_quien_ataca_primero(instancia_ia)

    contexto = crear_contexto(instancia_jugador, instancia_ia, orden_inicial)

    inicio_de_ronda(contexto)
    anotar(contexto, f"Ataca primero: {contexto.orden_ataca_primero}")

    if contexto.orden_ataca_primero == "jugador":
        ataque_jugador(contexto)
        if instancia_ia.sigue_vivo():
            ataque_ia(contexto)
    else:
        ataque_ia(contexto)
        if instancia_ia.sigue_vivo():
            ataque_jugador(contexto)
    fin_de_ronda(contexto)

    gano = instancia_ia.vida <= 0
    perdio = len(cartas_vivas(instancia_jugador.mazo)) == 0

    return {
        "orden": contexto.orden_ataca_primero,
        "registro_eventos": contexto.registro_eventos,
        "gano": gano,
        "perdio": perdio}
