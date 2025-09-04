from .carta import Carta

class Estructura(Carta):

    def __init__(self, nombre_carta: str, tipo_carta: str, vida_maxima: int, multiplicador_defensa: float, precio_carta: int, probabilidad_especial: float, ataque_base: int, multiplicador_ataque: float, habilidad_especial: str):
        
        super().__init__(nombre_carta, tipo_carta, vida_maxima, multiplicador_defensa, precio_carta, probabilidad_especial)

    def usar_habilidad_especial(self):

        print(f"{self.nombre_carta} intenta usar su habilidad especial.")

    def __str__(self) -> str:

        return (f"{self.nombre_carta} (estructura) - "
                f"Vida: {self.vida_actual}/{self.vida_maxima}, "
                f"Multiplicador Defensa: x{self.multiplicador_defensa}")
