from funciones.carta import Carta
from parametros import DANO_BOMBA, CANNON_ABILITY, CANNON_DECREASE, DIE_PROB, PROB_LAPIDA
from funciones.jugador import Jugador
from funciones.ia import IA
from funciones.leer_archivos import cargar_cartas, cargar_ias, cargar_multiplicadores

class Estructura(Carta):

    def __init__(self, nombre_carta: str, tipo_carta: str, vida_maxima: int, multiplicador_defensa: float, precio_carta: int, probabilidad_especial: float, ataque_base: int, multiplicador_ataque: float, habilidad_especial: str):
        
        super().__init__(nombre_carta, tipo_carta, vida_maxima, multiplicador_defensa, precio_carta, probabilidad_especial)
        
        self.ataque_base = ataque_base
        self.multiplicador_ataque = multiplicador_ataque
        self.habilidad_especial = habilidad_especial
        
    def usar_habilidad_especial(self):

        print(f"{self.nombre_carta} intenta usar su habilidad especial.")

    def __str__(self) -> str:

        return (f"{self.nombre_carta} (estructura) - "
                f"Vida: {self.vida_actual}/{self.vida_maxima}, "
                f"Multiplicador Defensa: x{self.multiplicador_defensa}")

    #habilidades

    #cañon

    def inicio_de_ronda(self, contexto):
    # ejemplo: bajar defensa de IA contra TROPAS y MIXTAS
        ia = contexto.instancia_ia
        ia.multiplicadores_defensa["tropa"] = max(0.0, ia.multiplicadores_defensa["tropa"] - CANNON_ABILITY)
        ia.multiplicadores_defensa["mixta"] = max(0.0, ia.multiplicadores_defensa["mixta"] - CANNON_ABILITY)
        contexto.registro_eventos.append("Gracias al Cañon la IA más vulnerable a ataques aliados esta ronda.")

    # TORRE IDE
    def antes_de_ataque_del_jugador(self, contexto):
        if contexto.orden_ataca_primero == "jugador":
            if contexto.generador_aleatorio() < DIE_PROB:
                contexto.instancia_ia._inhabilitada_esta_ronda = True
                contexto.registro_eventos.append("Gracias a la Torre IDE La IA queda inhabilitada y no atacará.")

    #RECOLECTOR DE AGUA

    def morir(self, contexto):
        if contexto.orden_ataca_primero == "ia":
            nueva = contexto.instancia_jugador.obtener_tropa_aleatoria_de_coleccion()
            if nueva:
                contexto.instancia_jugador.agregar_al_mazo(nueva)
                contexto.registro_eventos.append(f"El recolector hace que entre {nueva.nombre_carta} de inmediato.")
        else:
            # marcar para resolver al final según victoria/supervivencia
            self._pendiente_reemplazo = True

    def fin_de_ronda(self, contexto):
        if getattr(self, "_pendiente_reemplazo", False):
            if contexto.instancia_jugador.hay_alguna_carta_viva():
                nueva = contexto.instancia_jugador.obtener_tropa_aleatoria_de_coleccion()
                if nueva:
                    contexto.instancia_jugador.agregar_al_mazo(nueva)
                    contexto.registro_eventos.append(f"Recolector trae a {nueva.nombre_carta} por victoria/supervivencia.")
            self._pendiente_reemplazo = False

    #HORNO

    def morir(self, contexto):
        nueva = crear_espiritu_igneo()
        if contexto.orden_ataca_primero == "ia":
            contexto.instancia_jugador.agregar_al_mazo(nueva)
            contexto.registro_eventos.append("El Horno hace que entre un Espíritu Ígneo de inmediato.")
        else:
            self._pendiente_reemplazo = nueva

    def fin_de_ronda(self, contexto):
        if getattr(self, "_pendiente_reemplazo", None):
            if contexto.instancia_jugador.hay_alguna_carta_viva():
                contexto.instancia_jugador.agregar_al_mazo(self._pendiente_reemplazo)
                contexto.registro_eventos.append("Gracias al horno entra un Espíritu Ígneo por victoria/supervivencia.")
            self._pendiente_reemplazo = None


    #LAPIDA

    def antes_de_recibir_dano(self, contexto) -> bool:
        if contexto.generador_aleatorio() < PROB_LAPIDA:
            contexto.registro_eventos.append("Lápida evitó el daño.")
            return True
        return False

    #TORRE BOMBA

    def morir(self, contexto):
        contexto.instancia_ia.recibir_dano(DANO_BOMBA, "estructura")
        contexto.registro_eventos.append(f"La Torre Bomba explotó {DANO_BOMBA} a la IA.")

