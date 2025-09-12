from funciones.carta import Carta
from parametros import CURE_PEPPA, DEF_CAB, PROB_LARRY_GOD, PROB_LARRY_MID, PROB_BARB, POWER_UP_BARB, PROB_FIRE, PROB_GLOBO, DANO_BOMBA, CANNON_ABILITY, CANNON_DECREASE, DIE_PROB, PROB_LAPIDA
from funciones.jugador import Jugador
from funciones.ia import IA
from funciones.leer_archivos import cargar_cartas, cargar_ias, cargar_multiplicadores

class Tropa(Carta):
    
    def __init__(self, nombre_carta: str, tipo_carta: str, vida_maxima: int, multiplicador_defensa: float, precio_carta: int, probabilidad_especial: float, ataque_base: int, multiplicador_ataque: float, habilidad_especial: str):
        
        super().__init__(nombre_carta, tipo_carta, vida_maxima, multiplicador_defensa, precio_carta, probabilidad_especial)
        
        self.ataque_base = ataque_base
        self.multiplicador_ataque = multiplicador_ataque
        self.habilidad_especial = habilidad_especial
        self.ataque = int(self.ataque_base)
        self.buff_caballero = False
        self.valores_originales_caballero = []
        self.ataque_barbaros = False
    
    
    def usar_habilidad_especial(self):
        
        print(f"{self.nombre_carta} intenta usar su habilidad especial.")

    

    def __str__(self):

        return (f"{self.nombre_carta} (tropa) - "
                f"Vida: {self.vida_actual}/{self.vida_maxima}, "
                f"Ataque: {self.ataque_base}, "
                f"Multiplicador Ataque: x{self.multiplicador_ataque}")
    
    ###########habilidades


    def atacar(self, contexto):
        if contexto.instancia_ia.vida <= 0:
            return
        
        #el bloqueo de Crok no ataca
        if getattr(self, "_turnos_inhabilitada", 0) > 0:
            contexto.registro_eventos.append(f"{self.nombre_carta} está inhabilitada ({self._turnos_inhabilitada} rondas restantes) y no ataca.")
            return

        nombre_normal = self.nombre_carta.strip().lower().replace(".", "")

        
        dano_base = int(round(self.ataque * self.multiplicador_ataque))
        if dano_base < 0:
            dano_base = 0

        if nombre_normal == "duendes":
            #oro por daño infligido
            vida_ia_antes = contexto.instancia_ia.vida
            contexto.instancia_ia.recibir_dano(dano_base, "tropa")
            vida_ia_despues = contexto.instancia_ia.vida

            dano_real_infligido = vida_ia_antes - vida_ia_despues
            if dano_real_infligido < 0:
                dano_real_infligido = 0

            contexto.instancia_jugador.oro_disponible += dano_real_infligido
            contexto.registro_eventos.append(f"Duendes atacan e infligen {dano_real_infligido}. Ganas {dano_real_infligido}G")

        elif nombre_normal == "peppa":
            #se cura al atacar como el pekka evo
            contexto.instancia_ia.recibir_dano(dano_base, "tropa")

            puntos_a_curar = int(round(CURE_PEPPA * self.vida_maxima))
            vida_final = self.vida_actual + puntos_a_curar
            if vida_final > self.vida_maxima:
                vida_final = self.vida_maxima
            self.vida_actual = vida_final

            contexto.registro_eventos.append(
                f"P.E.P.P.A. ataca y se cura {puntos_a_curar} "
                f"(vida ahora {self.vida_actual}/{self.vida_maxima})")

        elif nombre_normal == "montapatos":
            #ataca primero el jugador
            contexto.instancia_ia.recibir_dano(dano_base, "tropa")
            contexto.registro_eventos.append("Montapatos hace que ataques primero!")

        elif nombre_normal == "antimuros inguc":
            #se suicidan
            contexto.instancia_ia.recibir_dano(dano_base, "tropa")

            self.vida_actual = 0
            indice_busqueda = 0
            while indice_busqueda < len(contexto.instancia_jugador.mazo):
                carta_en_mazo = contexto.instancia_jugador.mazo[indice_busqueda]
                if carta_en_mazo is self:
                    contexto.instancia_jugador.mazo.pop(indice_busqueda)
                    break
                indice_busqueda += 1

            contexto.registro_eventos.append("Antimuros IngUC ataca y se autodestruye :O")

        elif nombre_normal == "caballero":
            #aplica buff
            contexto.instancia_ia.recibir_dano(dano_base, "tropa")

            self.buff_caballero = False
            self.valores_originales_caballero = []

            indice_carta = 0
            while indice_carta < len(contexto.instancia_jugador.mazo):
                carta_aliada = contexto.instancia_jugador.mazo[indice_carta]
                if carta_aliada.vida_actual > 0:
                    valor_original = carta_aliada.multiplicador_defensa
                    self.valores_originales_caballero.append((carta_aliada, valor_original))

                    nuevo_valor = valor_original - DEF_CAB
                    if nuevo_valor < 0.0:
                        nuevo_valor = 0.0
                    carta_aliada.multiplicador_defensa = nuevo_valor
                    self.buff_caballero = True
                indice_carta += 1

            if self.buff_caballero:
                porcentaje = int(DEF_CAB * 100)
                contexto.registro_eventos.append(f"El caballero aplica un {porcentaje}% al multiplicador_defensa de tus cartas vivas)")

        elif nombre_normal in ("maldecidor duende", "maldecidorduende"):
            
            contexto.instancia_ia.recibir_dano(dano_base, "tropa")
            dano_extra_por_alucinacion = int(round(contexto.instancia_ia.ataque * 0.5))
            if dano_extra_por_alucinacion < 0:
                dano_extra_por_alucinacion = 0
            contexto.instancia_ia.recibir_dano(dano_extra_por_alucinacion, "tropa")
            contexto.registro_eventos.append(f"Maldecidor Duende realiza un ataque extra por {dano_extra_por_alucinacion}.")

        elif nombre_normal == "barbaros":
            contexto.instancia_ia.recibir_dano(dano_base, "tropa")
            self.ataque_barbaros = True
            contexto.registro_eventos.append("Barbaros atacó")

        elif nombre_normal in ("espiritu igneo", "espirituigneo"):
            contexto.instancia_ia.recibir_dano(dano_base, "tropa")  
            contexto.registro_eventos.append("Espíritu Ígneo atacó")
        
        elif nombre_normal == "globo":
            contexto.instancia_ia.recibir_dano(dano_base, "tropa")
            contexto.registro_eventos.append("Globo atacó y si muere puede dejar bomba")


        elif nombre_normal in ("escuadron de esqueletos", "escuadrón de esqueletos"):
            if contexto.generador_aleatorio() < PROB_LARRY_GOD:
                multiplicador_golpe = 5 
            else:
                multiplicador_golpe = 1
            dano_total = int(round(self.ataque * self.multiplicador_ataque * multiplicador_golpe))
            contexto.instancia_ia.recibir_dano(dano_total, "tropa")

            if multiplicador_golpe == 5:
                contexto.registro_eventos.append("Escuadrón de esqueletos atacó x5")
            else:
                contexto.registro_eventos.append("Escuadrón de esqueletos atacó por 1")

        else:
            #ataque normal
            contexto.instancia_ia.recibir_dano(dano_base, "tropa")
            contexto.registro_eventos.append(f"{self.nombre_carta} ataca con {dano_base}")

    def antes_de_ataque_del_jugador(self, contexto):
        if self.nombre_carta.strip().lower() == "montapatos" and self.vida_actual > 0:
            contexto.orden_ataca_primero = "jugador"
            contexto.registro_eventos.append("Montapatos asegura que atacas primero!")

    def antes_de_recibir_dano(self, contexto) -> bool:
        nombre_normal = self.nombre_carta.strip().lower()
        #espiritu puede evadir daño
        if nombre_normal in ("espiritu igneo", "espirituigneo"):
            if contexto.generador_aleatorio() < PROB_FIRE:
                contexto.registro_eventos.append("Espíritu Ígneo evadió el daño")
                return True  #no hay daño

        #esqueletos pueden morir
        if nombre_normal in ("escuadron de esqueletos", "escuadrón de esqueletos"):
            if contexto.generador_aleatorio() < PROB_LARRY_MID:
                self.vida_actual = 0
                contexto.registro_eventos.append("Escuadrón de esqueletos murió instantáneamente :(")
                return True  #no hay daño, ya murió
        return False
    
    def morir(self, contexto):
        if self.nombre_carta.strip().lower() == "globo":
            if contexto.generador_aleatorio() < PROB_GLOBO:
                contexto.instancia_ia.recibir_dano(DANO_BOMBA, "tropa")
                contexto.registro_eventos.append(f"El globo explotó hizo {DANO_BOMBA} a la IA.")

    def inicio_de_ronda(self, contexto):
        if self.nombre_carta.strip().lower() != "caballero":
            return
        self.buff_caballero = False
        self.valores_originales_caballero = []

        i = 0
        while i < len(contexto.instancia_jugador.mazo):
            carta_aliada = contexto.instancia_jugador.mazo[i]
            if carta_aliada is not self and carta_aliada.tipo_carta == "tropa" and carta_aliada.vida_actual > 0:
                valor_original = carta_aliada.multiplicador_defensa
                self.valores_originales_caballero.append((carta_aliada, valor_original))
                nuevo_valor = valor_original - DEF_CAB
                if nuevo_valor < 0.0:
                    nuevo_valor = 0.0
                carta_aliada.multiplicador_defensa = nuevo_valor
                self.buff_caballero = True
            i += 1

        if self.buff_caballero:
            contexto.registro_eventos.append(f"El caballero aplica {int(DEF_CAB*100)}% al multiplicador_defensa de tus tropas por esta ronda")

    def fin_de_ronda(self, contexto):
        #revertir efectos del caballero
        if self.buff_caballero:
            j = 0
            while j < len(self.valores_originales_caballero):
                carta_aliada, valor_original = self.valores_originales_caballero[j]
                carta_aliada.multiplicador_defensa = valor_original
                j += 1
            self.buff_caballero = False
            self.valores_originales_caballero = []
            contexto.registro_eventos.append("Terminó el efecto del Caballero.")

        #si barbaros sobreviven al ataque
        if self.nombre_carta.strip().lower() == "barbaros":
            if self.ataque_barbaros and self.vida_actual > 0:
                if contexto.generador_aleatorio() < PROB_BARB:
                    incremento = int(round(self.ataque * POWER_UP_BARB))
                    self.ataque = self.ataque + incremento
                    contexto.registro_eventos.append(f"Los Barbaro se potencian en (+{incremento}). Su ataque ahora es: {self.ataque}") 
            self.ataque_barbaros = False
