from random import random, choice, sample
from .carta import Carta
from .leer_archivos import cargar_multiplicadores
import os
from funciones.jugador import Jugador


class IA:
    def __init__(self, nombre, vida_maxima, ataque, descripcion, probabilidad_especial, velocidad):
        self.nombre = nombre
        self.vida_maxima = int(vida_maxima)
        self.vida_ia = int(vida_maxima)
        self.ataque = int(ataque)
        self.descripcion = descripcion
        self.probabilidad_especial = float(probabilidad_especial)
        self.velocidad = float(velocidad)
        
        self.multiplicadores_ataque = {}
        self.multiplicadores_defensa = {}
        

        self.instancia_jugador = Jugador(nombre)
        
    @property
    def vida(self):
        return self.vida_ia
    
    @vida.setter
    def vida(self, valor ):
        valor = int(valor)
        if int(valor) < 0:
            self.vida_ia = 0
        elif valor > self.vida_maxima:
            self.vida_ia = self.vida_maxima
        else:
            self.vida_ia = valor

    
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

            elif i.tipo_carta == "tropa" and i.vida_actual > 0:
                cartas_tropa.append(i)
                

        if cartas_defensoras:
            daño_por_objetivo = round(self.ataque / numero_defensoras)
            for carta in cartas_defensoras:
                print(f"{self.nombre} ataca a {carta.nombre_carta} con {daño_por_objetivo} de daño dividido")
                carta.recibir_dano(daño_por_objetivo)

        else:
            for carta in cartas_tropa:
                print(f"{self.nombre} ataca a {carta.nombre_carta} con {self.ataque} de daño completo")
                carta.recibir_dano(self.ataque)        
    
    def inyectar_multiplicadores(self): ########
    
        lista_diccionarios_multiplicadores = cargar_multiplicadores()

        for fila in lista_diccionarios_multiplicadores:
            if fila["ia_nombre"] == self.nombre:
                tipo_carta = fila["carta_tipo"].strip().lower()
                self.multiplicadores_ataque[tipo_carta] = float(fila["multiplicador_ataque"])
                self.multiplicadores_defensa[tipo_carta] = float(fila["multiplicador_defensa"])
    
    def __str__(self):  # DEGBUG
        return (f"IA {self.nombre} | Vida: {self.vida}/{self.vida_maxima} | "
                f"Ataque: {self.ataque} | Velocidad: {self.velocidad} | "
                f"Probabilidad Especial: {self.probabilidad_especial}")
    

    #para toda esta seccion la cual era toda aleatroria busque referencias de la libreria random 
    # https://docs.python.org/3/library/random.html

    def usar_habilidad_especial(self, instancia_jugador):

        tirada = random()

        
        
        if tirada > self.probabilidad_especial:
            return False  # no se activo

        if self.nombre == "CatGPT":
            return self.habilidad_catgpt(instancia_jugador)

        elif self.nombre == "CowPilot":
            return self.habilidad_cowpilot(instancia_jugador)

        elif self.nombre == "Crok":
            return self.habilidad_crok(instancia_jugador)

        elif self.nombre == "DeepSheep":
            return self.habilidad_deepsheep(instancia_jugador)

        elif self.nombre == "Gemibee":
            return self.habilidad_gemibee()

        return False

    # habilidades

    def habilidad_catgpt(self, jugador):
        for carta in jugador.mazo:
            carta.multiplicador_ataque = 0.65
            carta.multiplicador_defensa = 0.65
        print("[CatGPT] Redujo multiplicadores de todas las cartas a 0.65")
        return True

    def habilidad_cowpilot(self, jugador):
        if len(jugador.mazo) < 2:
            return False
        
        
        indices = sample(range(len(jugador.mazo)), 2)
        referencia = choice(jugador.mazo)
        jugador.mazo[indices[0]] = referencia
        jugador.mazo[indices[1]] = referencia
        print("CowPilot Reemplazó dos cartas por copias de otra.")
        return True

    def habilidad_crok(self, jugador):
        if len(jugador.mazo) < 2:
            return False
        elegidas = sample(jugador.mazo, 2)
        for carta in elegidas:
            carta._turnos_inhabilitada = 3
        print("Crok Dos cartas quedaron inhabilitadas por 3 rondas.")
        return True

    def habilidad_deepsheep(self, jugador):    
        if not jugador.mazo:
            return False
        vida_max = 0
        for i in jugador.mazo:
            if i.vida_actual > vida_max:
                vida_max = i.vida_actual
        for j in jugador.mazo:
            j._vida_fake = vida_max
        print("DeepSheep ahora todas las cartas muestran la misma vida :O.")
        return True


    def habilidad_gemibee(self):
        for tipo in self.multiplicadores_ataque:
            self.multiplicadores_ataque[tipo] += 0.1
        for tipo in self.multiplicadores_defensa:
            self.multiplicadores_defensa[tipo] += 0.1
        print("Gemibee aumentó sus multiplicadores de ataque y defensa en +0.1")
        return True