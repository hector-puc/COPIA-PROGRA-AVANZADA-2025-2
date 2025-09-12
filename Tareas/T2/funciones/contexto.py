from random import random
import copy

class Contexto:
    def __init__(self, instancia_jugador, instancia_ia, lista_cartas_aliadas, orden_ataca_primero, generador_aleatorio, registro_eventos=None):
        
        self.instancia_jugador = instancia_jugador
        self.instancia_ia = instancia_ia
        self.lista_cartas_aliadas = lista_cartas_aliadas
        self.orden_ataca_primero = orden_ataca_primero  
        self.generador_aleatorio = generador_aleatorio 
        self.registro_eventos = registro_eventos


#https://stackoverflow.com/questions/4075190/what-is-how-to-use-getattr-in-python
#para saber si el atributo existe en la clase y no de errores xd que lo cargaba mal 

def velocidad(instancia_ia, cartas_activas_del_jugador):
    #montapatos
    for i in cartas_activas_del_jugador:
        if getattr(i, "nombre_carta", "").strip().lower() == "montapatos" and getattr(i, "vida_actual", 0) > 0:
            return "jugador"

    velocidad_ia = float(getattr(instancia_ia, "velocidad", 0.0))
    velocidad_jugador = random()
    if velocidad_jugador >= velocidad_ia:
        return "jugador"
    else:
        return "ia"
    

def ejecutar_ronda_ccontexto(instancia_jugador, instancia_ia, cartas_activas):

    orden_inicial = velocidad(instancia_ia, cartas_activas)

    objeto_contexto_ronda = Contexto(instancia_jugador = instancia_jugador, instancia_ia = instancia_ia, lista_cartas_aliadas = cartas_activas, orden_ataca_primero = orden_inicial,   generador_aleatorio = random, registro_eventos = [] )

    #https://micro.recursospython.com/recursos/la-funcion-hasattr.html
    #use hasttr para ver en caso de que la carta tenga ese modulo lo ocupe 

    for carta_en_juego in cartas_activas:
        if hasattr(carta_en_juego, "inicio_de_ronda"):
            carta_en_juego.inicio_de_ronda(objeto_contexto_ronda)

    
    for carta_en_juego in cartas_activas:
        if hasattr(carta_en_juego, "antes_de_ataque_del_jugador"):
            carta_en_juego.antes_de_ataque_del_jugador(objeto_contexto_ronda)

    objeto_contexto_ronda.registro_eventos.append(f"Ataca primero: {objeto_contexto_ronda.orden_ataca_primero}")


    if objeto_contexto_ronda.orden_ataca_primero == "jugador":


        for carta_en_juego in list(cartas_activas):
            if hasattr(carta_en_juego, "atacar"):
                carta_en_juego.atacar(objeto_contexto_ronda)

        # ia ataca si no fue bloqueada
        if not getattr(instancia_ia, "_inhabilitada_esta_ronda", False):
            instancia_ia.usar_habilidad_especial(instancia_jugador)
            multiplicadr_tropa = float(instancia_ia.multiplicadores_ataque.get("tropa"))
            multiplicador_estructura  = float(instancia_ia.multiplicadores_ataque.get("estructura"))
            multiplicador_mixta = float(instancia_ia.multiplicadores_ataque.get("mixta"))
            instancia_jugador.recibir_dano_de_ia(int(instancia_ia.ataque), multiplicadr_tropa, multiplicador_estructura, multiplicador_mixta, objeto_contexto_ronda)

    else:  #ia
        if not getattr(instancia_ia, "_inhabilitada_esta_ronda", False):
            instancia_ia.usar_habilidad_especial(instancia_jugador)
            multiplicadr_tropa = float(instancia_ia.multiplicadores_ataque.get("tropa"))
            multiplicador_estructura  = float(instancia_ia.multiplicadores_ataque.get("estructura"))
            multiplicador_mixta = float(instancia_ia.multiplicadores_ataque.get("mixta"))
            instancia_jugador.recibir_dano_de_ia(int(instancia_ia.ataque), multiplicadr_tropa, multiplicador_estructura, multiplicador_mixta, objeto_contexto_ronda)

        for carta_en_juego in list(cartas_activas):
            if hasattr(carta_en_juego, "atacar"):
                carta_en_juego.atacar(objeto_contexto_ronda)

    
    for carta_en_juego in list(cartas_activas):
        if hasattr(carta_en_juego, "fin_de_ronda"):
            carta_en_juego.fin_de_ronda(objeto_contexto_ronda)

    
    setattr(instancia_ia, "_inhabilitada_esta_ronda", False)
    for i in cartas_activas:
        if hasattr(i, "_turnos_inhabilitada"):
            if i._turnos_inhabilitada > 0:
                i._turnos_inhabilitada -= 1

    
    for mensaje in objeto_contexto_ronda.registro_eventos:
        print(mensaje)

    return
