from abc import ABC
from .carta import Carta
from parametros import CURE_PEPPA, DEF_CAB, PROB_LARRY_GOD, PROB_LARRY_MID, PROB_BARB, POWER_UP_BARB, PROB_FIRE, PROB_GLOBO,DANO_BOMBA, CANNON_ABILITY,CANNON_DECREASE


class Tropa(Carta):
    
    def __init__(self, nombre_carta: str, tipo_carta: str, vida_maxima: int, multiplicador_defensa: float, precio_carta: int, probabilidad_especial: float, ataque_base: int, multiplicador_ataque: float, habilidad_especial: str):
        
        super().__init__(nombre_carta, tipo_carta, vida_maxima, multiplicador_defensa, precio_carta, probabilidad_especial)
        
        self.ataque_base = ataque_base
        self.multiplicador_ataque = multiplicador_ataque
        self.habilidad_especial = habilidad_especial

    def atacar(self, ia_enemiga):

        dano_total = round(self.ataque_base * self.multiplicador_ataque)
        ia_enemiga.recibir_dano(dano_total, tipo_carta = "tropa")
        return dano_total
    
    def usar_habilidad_especial(self):
        
        print(f"{self.nombre_carta} intenta usar su habilidad especial.")

    

    def __str__(self):

        return (f"{self.nombre_carta} (tropa) - "
                f"Vida: {self.vida_actual}/{self.vida_maxima}, "
                f"Ataque: {self.ataque_base}, "
                f"Multiplicador Ataque: x{self.multiplicador_ataque}")
    
    ###########habilidades

    #DUENDES

    def atacar(self, contexto): 
        dano_predefensa = int(round(self.ataque * self.multiplicador_ataque))
        dano_real = contexto.instancia_ia.recibir_dano(dano_predefensa, tipo_carta_atacante = "tropa")
        contexto.instancia_jugador.oro += dano_real
        contexto.registro_eventos.append(f"Duendes +{dano_real}monedas por daño infligido.")

    #PEPPA

    def atacar(self, contexto):
        dano = int(round(self.ataque * self.multiplicador_ataque))
        contexto.instancia_ia.recibir_dano(dano, "tropa")
        puntos_cura = int(round(self.vida_maxima * CURE_PEPPA))
        self.vida = min(self.vida_maxima, self.vida + puntos_cura)
        contexto.registro_eventos.append(f"P.E.P.P.A. se cura {puntos_cura} HP al atacar.")
    
    #MONTAPATOS

    def antes_de_ataque_del_jugador(self, contexto):
        contexto.orden_ataca_primero = "jugador"
        contexto.registro_eventos.append("Gracias a MontaPatos el jugador atacará primero esta ronda.")

    #ANTIMUROS UC

    def atacar(self, contexto):
        dano = int(round(self.ataque * self.multiplicador_ataque))
        contexto.instancia_ia.recibir_dano(dano, "tropa")
        self.vida = 0
        contexto.registro_eventos.append("Antimuros Se elimina del mazo.")

    #CABALLERO

    def inicio_de_ronda(self, contexto):
        for carta in contexto.lista_cartas_aliadas:
            if carta is self: 
                continue
            if carta.tipo_carta == "tropa":
                carta.multiplicador_defensa *= (1.0 - DEF_CAB)  # si DEF_CAB es porcentaje de reducción de daño
                carta._buff_def_cab_aplicado = True
        contexto.registro_eventos.append("Caballero 'Buff DEF' a otras tropas.")

    def fin_de_ronda(self, contexto):
        # revertir
        for carta in contexto.lista_cartas_aliadas:
            if getattr(carta, "_buff_def_cab_aplicado", False):
                carta.multiplicador_defensa /= (1.0 - DEF_CAB)
                carta._buff_def_cab_aplicado = False

    #MALDECIDOR DUENDE

    def atacar(self, contexto):
        dano1 = int(round(self.ataque * self.multiplicador_ataque))
        contexto.instancia_ia.recibir_dano(dano1, "tropa")
        dano2 = int(round(contexto.instancia_ia.ataque * 0.5))  # mitad del ataque base IA (pre-multiplicadores)
        contexto.instancia_ia.recibir_dano(dano2, "tropa")
        contexto.registro_eventos.append(f"MaldecidorDuende Ataca extra por {dano2}.")


    #ESCUADRON ESQUELETOS
    def atacar(self, contexto):
        factor = 5 if contexto.generador_aleatorio() < PROB_LARRY_GOD else 1
        dano = int(round(self.ataque * self.multiplicador_ataque * factor))
        contexto.instancia_ia.recibir_dano(dano, "tropa")
        if factor == 5:
            contexto.registro_eventos.append("Larry VAMOS! GOLPE x5!")

    def antes_de_recibir_dano(self, contexto) -> bool:
        if contexto.generador_aleatorio() < PROB_LARRY_MID:
            self.vida = 0
            contexto.registro_eventos.append("Larrys murieron instantáneamente :((")
            return True 
        return False


    #BARBAROS

    def atacar(self, contexto):
        self._barb_ataco_esta_ronda = True
        dano = int(round(self.ataque * self.multiplicador_ataque))
        #contexto.instancia_ia.recibir_dano(dano, "tropa")

    def fin_de_ronda(self, contexto):
        if getattr(self, "_barb_ataco_esta_ronda", False) and self.vida > 0:
            if contexto.generador_aleatorio() < PROB_BARB:
                incremento = self.ataque * POWER_UP_BARB
                self.ataque = int(round(self.ataque + incremento))
                contexto.registro_eventos.append(f"Bárbaros! nuevo ataque!: {self.ataque}.")
        self._barb_ataco_esta_ronda = False
    
    #ESPERITO IGNEO
    # 
    def antes_de_recibir_dano(self, contexto) -> bool:
        if contexto.generador_aleatorio() < PROB_FIRE:
            contexto.registro_eventos.append("Espíritu Ígneo evadió el daño.")
            return True
        return False
    
    #GLOBO

    def morir(self, contexto):
        if contexto.generador_aleatorio() < PROB_GLOBO:
            contexto.instancia_ia.recibir_dano(DANO_BOMBA, "tropa")
            contexto.registro_eventos.append(f"Globo. Bomba! {DANO_BOMBA} de daño a la IA.")
    

