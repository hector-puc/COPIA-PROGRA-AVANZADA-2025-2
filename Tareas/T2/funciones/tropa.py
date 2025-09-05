from abc import ABC
from .carta import Carta

class Tropa(Carta):
    
    def __init__(self, nombre_carta: str, tipo_carta: str, vida_maxima: int, multiplicador_defensa: float, precio_carta: int, probabilidad_especial: float, ataque_base: int, multiplicador_ataque: float, habilidad_especial: str):
        
        super().__init__(nombre_carta, tipo_carta, vida_maxima, multiplicador_defensa, precio_carta, probabilidad_especial)
        
        self.ataque_base = ataque_base
        self.multiplicador_ataque = multiplicador_ataque
        self.habilidad_especial = habilidad_especial

    def atacar(self, ia_enemiga):

        dano_total = round(self.ataque_base * self.multiplicador_ataque)
        ia_enemiga.recibir_dano(dano_total, tipo_carta="tropa")
        return dano_total
    
    def usar_habilidad_especial(self):
        
        print(f"{self.nombre_carta} intenta usar su habilidad especial.")

    

    def __str__(self):

        return (f"{self.nombre_carta} (tropa) - "
                f"Vida: {self.vida_actual}/{self.vida_maxima}, "
                f"Ataque: {self.ataque_base}, "
                f"Multiplicador Ataque: x{self.multiplicador_ataque}")
    

    
    