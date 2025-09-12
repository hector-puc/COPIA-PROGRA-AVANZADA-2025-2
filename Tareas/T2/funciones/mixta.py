from .carta import Carta
from .tropa import Tropa
from .estructura import Estructura
from random import random
from parametros import COSTO_COMBINACION

class Mixta(Tropa):

    def __init__(self, instancia_tropa: Tropa, instancia_estructura: Estructura):

        if not isinstance(instancia_tropa, Tropa):
            print("Tienes que elegir una tropa válida")
            pass
        if not isinstance(instancia_estructura, Estructura):
            print("Tienes que elegir una estructura válida")
            pass

        self.tropa_base = instancia_tropa
        self.estructura_base = instancia_estructura
        self.respaldo_mixta = None

        vida_maxima_combinada = int(round(instancia_estructura.vida_maxima + (instancia_tropa.vida_maxima // 2)))

        #menor multiplicador recibe menos daño
        multiplicador_defensa_combinado = min(instancia_tropa.multiplicador_defensa, instancia_estructura.multiplicador_defensa)
        multiplicador_ataque_combinado = instancia_tropa.multiplicador_ataque
        ataque_base_combinado = instancia_tropa.ataque_base
        probabilidad_especial_combinada = ((instancia_tropa.probabilidad_especial + instancia_estructura.probabilidad_especial) / 2.0 * 1.10)
        nombre_carta = f"{instancia_tropa.nombre_carta}-{instancia_estructura.nombre_carta}"
        habilidad_especial_combinada = f"{instancia_tropa.usar_habilidad_especial} + {instancia_estructura.usar_habilidad_especial}"

        
        super().__init__(
            nombre_carta = nombre_carta,
            tipo_carta = "mixta",
            vida_maxima = vida_maxima_combinada,
            multiplicador_defensa = multiplicador_defensa_combinado,
            precio_carta = COSTO_COMBINACION,
            probabilidad_especial = probabilidad_especial_combinada,
            ataque_base = ataque_base_combinado,
            multiplicador_ataque = multiplicador_ataque_combinado,
            habilidad_especial = habilidad_especial_combinada
            )

        

    def usar_habilidad_especial(self):

        if random() < self.probabilidad_especial:
            print(f"{self.nombre_carta} ha utilizado habilidades especiales!")    

            self.tropa_base.usar_habilidad_especial()
            self.estructura_base.usar_habilidad_especial()
        else:
            print(f"{self.nombre_carta} no activo su habilidad :(")


    def __str__(self):
        return (f"{self.nombre_carta} (mixta) - "
                f"Vida: {self.vida_actual}/{self.vida_maxima}, "
                f"Ataque: {self.ataque_base}, "
                f"Multiplicador Ataque: x{self.multiplicador_ataque}, "
                f"Multiplicador Defensa: x{self.multiplicador_defensa}, "
                f"Probabilidad Especial: {self.probabilidad_especial}%")
    

    #esto ejecuta las habilidades de inicio de ronda de la estructura

    def inicio_de_ronda(self, contexto):
        if hasattr(self.estructura_base, "inicio_de_ronda"):
            defensa_antes = getattr(self.estructura_base, "multiplicador_defensa", self.multiplicador_defensa)
            self.estructura_base.inicio_de_ronda(contexto)
            self.multiplicador_defensa = getattr(self.estructura_base, "multiplicador_defensa", defensa_antes)

    def antes_de_recibir_dano(self, contexto) -> bool:
        if hasattr(self.estructura_base, "antes_de_recibir_dano"):
            if self.estructura_base.antes_de_recibir_dano(contexto):
                return True
        return False

    def morir(self, contexto):
        if hasattr(self.estructura_base, "morir"):
            self.estructura_base.morir(contexto)

    def fin_de_ronda(self, contexto):
        if hasattr(self.estructura_base, "fin_de_ronda"):
            self.estructura_base.fin_de_ronda(contexto)
        self.multiplicador_defensa = getattr(self.estructura_base, "multiplicador_defensa", self.multiplicador_defensa)

