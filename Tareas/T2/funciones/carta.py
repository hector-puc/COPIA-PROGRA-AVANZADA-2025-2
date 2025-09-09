from abc import ABC, abstractmethod

class Carta(ABC):

    def __init__(self, nombre_carta: str, tipo_carta: str, vida_maxima: int, multiplicador_defensa: float, precio_carta: int, probabilidad_especial: float):
        self.nombre_carta = nombre_carta
        self.tipo_carta = tipo_carta 
        self.vida_maxima = vida_maxima
        self.vida_actual = vida_maxima
        self.multiplicador_defensa = multiplicador_defensa
        self.precio_carta = precio_carta
        self.probabilidad_especial = probabilidad_especial

    def recibir_dano(self, cantidad_dano: int):

        dano_final = round(cantidad_dano * self.multiplicador_defensa)
        self.vida_actual -= dano_final

        if self.vida_actual <= 0:
            self.vida_actual = 0

        return dano_final
    
    @property
    def vida(self):
        return self.vida
    
    @vida.setter
    def vida(self, valor ):
        if int(valor) < 0:
            self.vida = 0
        elif int(valor) > self.vida_maxima:
            self.vida = self.vida_maxima
        else:
            self.vida = int(valor)


    @abstractmethod
    def usar_habilidad_especial(self):
        pass

    def __str__(self):
        return (f"{self.nombre_carta} ({self.tipo_carta}) - "
            f"Vida: {self.vida_actual}/{self.vida_maxima}, "
            f"Defensa: x{self.multiplicador_defensa}, "
            f"Precio: {self.precio_carta}, "
            f"Probablididad especial: {self.probabilidad_especial}")
    
    #habilidades

    def puede_atacar(self) -> bool:
        return False

    def on_inicio_de_ronda(self, contexto): 
        pass
    def on_antes_de_ataque_del_jugador(self, contexto): 
        pass
    def on_atacar(self, contexto): 
        pass
    def on_antes_de_recibir_dano(self, contexto) -> bool:
        return False
    def on_morir(self, contexto): 
        pass
    def on_fin_de_ronda(self, contexto): 
        pass
    

