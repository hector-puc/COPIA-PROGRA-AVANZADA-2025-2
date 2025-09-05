from random import random
from .carta import Carta
from .leer_archivos import cargar_multiplicadores
import os

class IA:
    def __init__(self, nombre, vida_maxima, ataque, descripcion, probabilidad_especial, velocidad):
        self.nombre = nombre
        self.vida_maxima = int(vida_maxima)
        self.vida = int(vida_maxima)
        self.ataque = int(ataque)
        self.descripcion = descripcion
        self.probabilidad_especial = float(probabilidad_especial)
        self.velocidad = float(velocidad)
        
        self.multiplicadores_ataque = {}
        self.multiplicadores_defensa = {}


    def sigue_vivo(self):
        if self.vida > 0:
            return True
        else:
            return False
        
    def recibir_dano(self, dano_total, tipo_carta):
        tipo_atacante = tipo_carta.lower()

        if tipo_atacante in self.multiplicadores_defensa:
            multiplicador_de_defensa = self.multiplicadores_defensa[tipo_atacante]
        else:
            multiplicador_de_defensa = 1.0

        dano_entero = int(round(dano_total * multiplicador_de_defensa))

        if self.vida - dano_entero < 0:
            self.vida = 0
        else:
            self.vida -= dano_entero
    
        print(f"La IA: {self.nombre} recibió {dano_entero} puntos de daño!")

        return dano_entero
    
    def atacar(self, lista_objetivos):
        if not self.sigue_vivo():
            return
        
        cartas_defensoras = []
        cartas_tropa = []
        numero_defensoras = 0

        for i in lista_objetivos:
            if i.tipo_carta == "estructura" and i.vida > 0 or i.tipo_carta == "mixta" and i.vida > 0:
                cartas_defensoras.append(i)
                numero_defensoras += 1

            elif i.tipo_carta == "tropa" and i.vida > 0:
                cartas_tropa.append(i)
                

        if cartas_defensoras:
            daño_por_objetivo = round(self.ataque / numero_defensoras)
            for carta in cartas_defensoras:
                print(f"{self.nombre} ataca a {carta.nombre_carta} con {daño_por_objetivo} de daño dividido")
                carta.recibir_dano(daño_por_objetivo, tipo_atacante="ia")

        else:
            for carta in cartas_tropa:
                print(f"{self.nombre} ataca a {carta.nombre_carta} con {self.ataque} de daño completo")
                carta.recibir_dano(self.ataque, tipo_atacante="ia")        
    
    def inyectar_multiplicadores(diccionario_ias, lista_multiplicadores): ########
    
        for registro in lista_multiplicadores:
            
            nombre_de_ia = registro["ia_nombre"]                 
            tipo_de_carta = registro["carta_tipo"].lower()
            multiplicador_de_ataque = float(registro["multiplicador_ataque"])
            multiplicador_de_defensa = float(registro["multiplicador_defensa"])

            if nombre_de_ia in diccionario_ias:
                instancia_ia = diccionario_ias[nombre_de_ia]

                instancia_ia.multiplicadores_ataque[tipo_de_carta] = multiplicador_de_ataque
                instancia_ia.multiplicadores_defensa[tipo_de_carta] = multiplicador_de_defensa
            else:
                pass
    
    def usar_habilidad_especial(self, instancia_jugador):
        tirada = random()
        if tirada < self.probabilidad_especial:
            return True
        return False
    
    def __str__(self) -> str:  # DEGBUG
        return (f"IA {self.nombre} | Vida: {self.vida}/{self.vida_maxima} | "
                f"Ataque: {self.ataque} | Velocidad: {self.velocidad} | "
                f"Probabilidad Especial: {self.probabilidad_especial}")