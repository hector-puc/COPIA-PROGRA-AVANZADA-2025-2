from random import random

class Contexto:
    def __init__(self, instancia_jugador, instancia_ia, lista_cartas_aliadas, orden_ataca_primero, generador_aleatorio, registro_eventos=None):
        
        self.instancia_jugador = instancia_jugador
        self.instancia_ia = instancia_ia
        self.lista_cartas_aliadas = lista_cartas_aliadas
        self.orden_ataca_primero = orden_ataca_primero  
        self.generador_aleatorio = generador_aleatorio 
        self.registro_eventos = registro_eventos

def velocidad(instancia_ia, cartas_activas):
    velocidad_ia = getattr(instancia_ia, "velocidad", 0.0)
    velocidad_jugador = random()
    if velocidad_jugador >= velocidad_ia:
        orden = "jugador"
    elif velocidad_jugador < velocidad_ia:
        orden = "ia"
    return orden
    

def ejecutar_ronda_ccontexto(instancia_jugador, instancia_ia, lista_cartas_activas_del_jugador):

    orden_inicial = velocidad(instancia_jugador, instancia_ia, lista_cartas_activas_del_jugador)
    objeto_contexto_ronda = Contexto(
        instancia_jugador=instancia_jugador,
        instancia_ia=instancia_ia,
        lista_cartas_aliadas=lista_cartas_activas_del_jugador,
        orden_ataca_primero=orden_inicial,  
        generador_aleatorio=random,
        registro_eventos=[]
    )

    #https://micro.recursospython.com/recursos/la-funcion-hasattr.html
    #use hasttr para ver en caso de que la carta tenga ese modulo lo ocupe 

    for carta_en_juego in lista_cartas_activas_del_jugador:
        if hasattr(carta_en_juego, "inicio_de_ronda"):
            carta_en_juego.inicio_de_ronda(objeto_contexto_ronda)

    
    for carta_en_juego in lista_cartas_activas_del_jugador:
        if hasattr(carta_en_juego, "antes_de_ataque_del_jugador"):
            carta_en_juego.antes_de_ataque_del_jugador(objeto_contexto_ronda)

    objeto_contexto_ronda.registro_eventos.append(f"Ataca primero: {objeto_contexto_ronda.orden_ataca_primero}")

    #JUGADOR USA TODAS LAS CARTAS CON ATACAR

    if objeto_contexto_ronda.orden_ataca_primero == "jugador":
        
        for carta_en_juego in list(lista_cartas_activas_del_jugador):
            if hasattr(carta_en_juego, "atacar"):
                carta_en_juego.atacar(objeto_contexto_ronda)

        # ia ataca si no fue bloqueada
        if not getattr(instancia_ia, "_inhabilitada_esta_ronda", False):
            instancia_ia.atacar(lista_cartas_activas_del_jugador)

    else:  # IA primero
        if not getattr(instancia_ia, "_inhabilitada_esta_ronda", False):
            instancia_ia.atacar(lista_cartas_activas_del_jugador)

        for carta_en_juego in list(lista_cartas_activas_del_jugador):
            if hasattr(carta_en_juego, "atacar"):
                carta_en_juego.atacar(objeto_contexto_ronda)

    
    for carta_en_juego in list(lista_cartas_activas_del_jugador):
        if hasattr(carta_en_juego, "fin_de_ronda"):
            carta_en_juego.fin_de_ronda(objeto_contexto_ronda)

    
    setattr(instancia_ia, "_inhabilitada_esta_ronda", False)

    
    for mensaje in objeto_contexto_ronda.registro_eventos:
        print(mensaje)

    
    return
