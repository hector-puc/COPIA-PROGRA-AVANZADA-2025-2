from .carta import Carta

class Jugador:
    def __init__(self, nombre_jugador: str):
        
        self.nombre_jugador = nombre_jugador
        self.oro_disponible = 15

        #15 de oro inicial
        
        self.coleccion = []
        self.mazo = []    

        #estadisticas opcionales
        self.rondas_ganadas = 0
        self.rondas_totales = 0

    def agregar_carta_a_coleccion(self, objeto_carta):
        self.coleccion.append(objeto_carta)

    def mover_carta_de_coleccion_a_mazo(self, indice_en_coleccion: int) -> bool:
        # si la mueve retorna true sino no
        if 0 <= indice_en_coleccion < len(self.coleccion):
            if len(self.mazo) >= 5:
                return False
            carta_seleccionada = self.coleccion[indice_en_coleccion]
            self.mazo.append(carta_seleccionada)
            return True
        return False
    
    def obtener_estructuras_y_mixtas_vivas(self):
        estructuras_vivas = []
        for i in self.mazo:
            if i.vida_actual > 0 and i.tipo_carta in ("estructura", "mixta"):
                estructuras_vivas.append(i)
        return estructuras_vivas


    def cartas_vivas(self):
        vivas = []
        for i in self.mazo:
            if i.vida_actual > 0:
                vivas.append(i)
        return vivas
    
    def remover_carta_muerta_del_mazo(self, objeto_carta: Carta):
        
        if objeto_carta in self.mazo and objeto_carta.vida_actual <= 0:
            self.mazo.remove(objeto_carta)

    def atacar(self, ia_enemiga) -> int:

        dano_total_acumulado_en_esta_fase = 0

        for objeto_carta in self.cartas_vivas():
            if objeto_carta.tipo_carta in ("tropa", "mixta"):
                dano_carta = objeto_carta.atacar(ia_enemiga)
                dano_total_acumulado_en_esta_fase += int(round(dano_carta))

        return dano_total_acumulado_en_esta_fase

#defensa jugador

    def recibir_dano_de_ia(self, dano_total: int, multiplicador_ataque_tropa: float, multiplicador_ataque_estructura: float, multiplicador_mixta: float, contexto):

        dano_total_efectivo = 0
        blanco_prioritario = self.obtener_estructuras_y_mixtas_vivas() 

        if hasattr(carta_objetivo, "antes_de_recibir_dano"):
            if carta_objetivo.antes_de_recibir_dano(contexto):
                return

        if len(blanco_prioritario) > 0:
            danio_base_por_carta = dano_total / len(blanco_prioritario)

        
            for carta_objetivo in (blanco_prioritario):
                if carta_objetivo.tipo_carta == "estructura":
                    dano_contra_esta_carta = danio_base_por_carta * multiplicador_ataque_estructura
                elif carta_objetivo.tipo_carta == "mixta":
                    dano_contra_esta_carta = danio_base_por_carta * multiplicador_mixta

                # cada carta tiene su propia defensa
                dano_en_esta_carta = carta_objetivo.recibir_dano(int(round(dano_contra_esta_carta)))
                dano_total_efectivo += dano_en_esta_carta

                # si murio se va del mazo
                if carta_objetivo.vida_actual <= 0:
                    carta_objetivo.morir(contexto)
                    self.remover_carta_muerta_del_mazo(carta_objetivo)

            return dano_total_efectivo

        #como el enunciado si el reparto es equitativo entre las tropas o solo a una lo hice para que sea reparto equitativo
        
        lista_tropas_vivas = []
        for i in self.cartas_vivas():
            if i.tipo_carta == "tropa":
                lista_tropas_vivas.append(i)
            
        if len(lista_tropas_vivas) == 0:
            return 0

        dano_base_por_tropa = dano_total / len(lista_tropas_vivas)

        for carta_tropa in (lista_tropas_vivas):
            dano_contra_tropa = dano_base_por_tropa * multiplicador_ataque_tropa
            dano_en_tropa = carta_tropa.recibir_dano(int(round(dano_contra_tropa)))
            dano_total_efectivo += dano_en_tropa

            if carta_tropa.vida_actual <= 0:
                self.remover_carta_muerta_del_mazo(carta_tropa)

        return dano_total_efectivo

    def agregar_al_mazo(self, objeto_carta):
        if objeto_carta in self.coleccion and objeto_carta not in self.mazo and len(self.mazo) < 5:
            self.coleccion.remove(objeto_carta)
            self.mazo.append(objeto_carta)
            return True
        return False

    def hay_alguna_carta_viva(self):
        for i in self.mazo:
            if getattr(i, "vida_actual", 0) > 0: #ANTI BUGS
                return True
        return False

    def obtener_tropa_aleatoria_de_coleccion(self): #retorna la primera tropa q encuentre
        for i in self.coleccion:
            if getattr(i, "tipo_carta", "").lower() == "tropa":
                return i
        return None

