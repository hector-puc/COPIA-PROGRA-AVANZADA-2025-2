from jugador import recibir_dano_de_ia
from random import random

def cartas_vivas(mazo):
    vivas = []
    for i in mazo:
        if getattr(i, "vida_Actual", 0) > 0:
            vivas.append(i)
        
    return vivas

def estructuras_y_mixtas_vivas(mazo):
    defensivas = []
    for i in mazo:
        tipo = getattr (i, "tipo_carta").lower().strip()
        if tipo in ("estructura", "mixta") and getattr(i, "vida_actual", 0) > 0:
            defensivas.append(i)
    return defensivas

def tropas_vivas(mazo):
    tropas = []
    for i in mazo:
        tipo = getattr (i, "tipo_carta").lower().strip()
        if tipo in ("tropa", "") and getattr(i, "vida_actual", 0) > 0:
            tropas.append(i)
    return tropas

def decidir_quien_ataca_primero(ia, montapatos_ver):
    
    if montapatos_ver:
        return "jugador"
    velocidad_ia = getattr(ia, "velocidad")

    velocidad_jugador = random()
    if velocidad_jugador >= velocidad_ia:
        return "jugador"
    else:
        return "ia"
    
def montapatos_ver(mazo):
    for i in mazo:
        nombre = getattr(i, "nombre_carta").lower().strip()
        if nombre == "montapatos" and getattr(i, "vida_actual", 0) > 0: #si el montapatos esta vivo le da el turno al jugador
            return True
    return False

def habilidad(carta, nombre_habilidad): #REVISAR ESTA FUNCION
    if hasattr(carta, nombre_habilidad): #si tiene la habilidad la activa pero tiene que tener contexto
        metodo = getattr(carta, nombre_habilidad)
        metodo(contexto)
        return True
    return False

def crear_contexto(instancia_jugador, instancia_ia, mazo_activas, orden_ataca_primero):
    contexto = {"instancia_jugador": instancia_jugador, "instancia_ia": instancia_ia, "mazo_activas": mazo_activas, "orden_ataca_primero": orden_ataca_primero, "registro_eventos": []}
    return contexto

def anotar(contexto, mensaje):
    lista = contexto["registro_eventos"]
    lista.append(mensaje)

def dano_ia_jugador(instancia_jugador, instancia_ia, dano_total):
    mazo = instancia_jugador.mazo
    objetivo_defensa = estructuras_y_mixtas_vivas(mazo)

    dano = 0

    if len(objetivo_defensa) > 0:
        dano_unitario = dano_total / len(objetivo_defensa)
        indice = 0

        while indice < len(objetivo_defensa):
            carta = objetivo_defensa[indice] #esto es para las cartas que peuden evitar daño

            evitar = False
            if hasattr(carta, "antes_de_recibir_dano"):
                evitar = bool(carta.on_antes_de_recibir_dano({"instancia_jugador": instancia_jugador, "instancia_ia": instancia_ia}))
            if not evitar:
                dano_ronda = int(round(dano_unitario))
                carta.recibir_dano(dano_ronda)
                dano += dano_ronda

            if getattr(carta, "vida_actual", 0) <= 0:
                if hasattr(carta, "morir"):
                    carta.morir({"instancia_jugador": instancia_jugador, "instancia_ia": instancia_ia})
            indice += 1

        return dano

#si no hay estructuras o mixtas
    blanco_tropas = tropas_vivas(mazo)
    if len(blanco_tropas) == 0:
        return 0
    
    dano_por_tropa = dano_total / len(blanco_tropas)

    indice_2 = 0
    while indice_2 < len(blanco_tropas):
        tropa = blanco_tropas[indice_2]
        evitar = False
        if hasattr(tropa, "antes_de_recibir_dano"):
            evitar = bool(tropa.antes_de_recibir_dano({"instancia_jugador": instancia_jugador, "instancia_ia": instancia_ia}))

        if not evitar:
            dano_en_tropa = int(round(dano_por_tropa))
            tropa.recibir_dano(dano_en_tropa)
            dano += dano_en_tropa

        
        if hasattr(tropa, "morir"):
            tropa.morir({"instancia_jugador": instancia_jugador, "instancia_ia": instancia_ia})
        indice_2 += 1

    return dano     

def ataque_jugador(contexto):
    jugador = contexto["instancia_jugador"]
    ia = contexto["instancia_ia"]
    mazo = cartas_vivas(jugador.mazo)

    indice = 0

    while indice < len(mazo):   
        habilidad(mazo[indice], "inicio_ronda", contexto)
        indice += 1

    indice_2 = 0
    while indice_2 < len(mazo):
        habilidad(mazo[indice_2], "antes_de_ataque_del_jugador", contexto)
        indice_2 += 1
    
    
    indice_3 = 0
    while indice_3 < len(mazo):
        carta = mazo[t]
        tipo = str(getattr(carta, "tipo_carta", "")).lower()
        if tipo in ("tropa", "mixta") and getattr(carta, "vida_actual", 0) > 0:
            hizo_habilidad = habilidad(carta, "on_atacar", contexto)
            if not hizo_habilidad:
                ataque_base = int(getattr(carta, "ataque_base", 0))
                multi_ataque = float(getattr(carta, "multiplicador_ataque", 1.0))
                dano = int(round(ataque_base * multi_ataque))
                if dano > 0:
                    ia.recibir_dano(dano, "tropa")
        indice_3 += 1

    
    def ataque_ia(contexto):
        jugador = contexto["instancia_jugador"]
        ia = contexto["instancia_ia"]

        if hasattr(ia, "usar_habilidad_especial"):
            ia.usar_habilidad_especial(jugador)

        if not ia.sigue_vivo():
            return

        dano_total_ia = int(getattr(ia, "ataque", 0))
        if dano_total_ia <= 0:
            return

        recibir_dano_de_ia(jugador, ia, dano_total_ia) #REVISAR LINEA

    def fin_de_ronda(contexto):
        jugador = contexto["instancia_jugador"]
        ia = contexto["instancia_ia"]
        mazo = cartas_vivas(jugador.mazo)

        indice = 0
        while indice < len(mazo):
            habilidad(mazo[indice], "on_fin_de_ronda", contexto)
            indice += 1


    def ejecutar_ronda(instancia_jugador, instancia_ia):
        
        jugador_tiene_montapatos = montapatos_ver(instancia_jugador.mazo)

        orden = decidir_quien_ataca_primero(instancia_ia, jugador_tiene_montapatos)
        contexto = crear_contexto(instancia_jugador, instancia_ia, instancia_jugador.mazo, orden)

        anotar(contexto, f"Ataca primero: {orden}")

        if orden == "jugador":
            ataque_jugador(contexto)
            if instancia_ia.sigue_vivo():
                ataque_ia(contexto)
        else:
            ataque_ia(contexto)
            if instancia_ia.sigue_vivo():
                ataque_jugador(contexto)

        fin_de_ronda(contexto)

        gano = False
        perdio = False
        if instancia_ia.vida <= 0:
            gano = True
        #el jugador pierde si todas sus cartas mueren
        hay_vivas = False
        indice = 0
        while indice < len(instancia_jugador.mazo):
            if getattr(instancia_jugador.mazo[indice], "vida_actual", 0) > 0:
                hay_vivas = True
                break
            indice += 1
        if not hay_vivas:
            perdio = True

        return {"orden": orden, "registro_eventos": contexto["registro_eventos"], "gano": gano, "perdio": perdio}
