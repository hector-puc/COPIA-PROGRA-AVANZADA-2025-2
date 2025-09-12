from .carta import Carta
from parametros import DINERO_INICIAL

class Jugador:
    def __init__(self, nombre_jugador: str):
        
        self.nombre_jugador = nombre_jugador
        self.oro_disponible = DINERO_INICIAL

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
            self.coleccion.remove(carta_seleccionada)
            return True
        return False
    
    def obtener_estructuras_y_mixtas_vivas(self):
        estructuras_vivas = []
        for i in self.mazo:
            if i.vida_actual > 0 and i.tipo_carta in ("estructura", "mixta"):
                if getattr(i, "_turnos_inhabilitada", 0) == 0: #crok inhabilita cosas
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

        

        if len(blanco_prioritario) > 0:
            danio_base_por_carta = dano_total / len(blanco_prioritario)

        
            for carta_objetivo in (blanco_prioritario):
                if hasattr(carta_objetivo, "antes_de_recibir_dano"):
                    if carta_objetivo.antes_de_recibir_dano(contexto):
                        continue
            
                if carta_objetivo.tipo_carta == "estructura":
                    dano_contra_esta_carta = danio_base_por_carta * multiplicador_ataque_estructura
                elif carta_objetivo.tipo_carta == "mixta":
                    dano_contra_esta_carta = danio_base_por_carta * multiplicador_mixta

                #cada carta tiene su propia defensa
                dano_en_esta_carta = carta_objetivo.recibir_dano(int(round(dano_contra_esta_carta)))
                dano_total_efectivo += dano_en_esta_carta

                #si murio se va del mazo
                if carta_objetivo.vida_actual <= 0:
                    carta_objetivo.morir(contexto)
                    self.remover_carta_muerta_del_mazo(carta_objetivo)

            return dano_total_efectivo

        #si no hay estructuras o mixtas vivas

        lista_tropas_vivas = []
        for i in self.cartas_vivas():
            if i.tipo_carta == "tropa" and getattr(i, "_turnos_inhabilitada", 0) == 0: #crok inhabilita cartas
                lista_tropas_vivas.append(i)
            
        if len(lista_tropas_vivas) == 0:
            return 0

        dano_base_por_tropa = dano_total * multiplicador_ataque_tropa

        indice_tropa = 0
        while indice_tropa < len(lista_tropas_vivas):
            carta_tropa = lista_tropas_vivas[indice_tropa]
            dano_contra_tropa = dano_base_por_tropa
            dano_en_tropa = carta_tropa.recibir_dano(int(round(dano_contra_tropa)))
            dano_total_efectivo += dano_en_tropa

            if carta_tropa.vida_actual <= 0:
                self.remover_carta_muerta_del_mazo(carta_tropa)
            indice_tropa += 1

        return dano_total_efectivo

    def agregar_al_mazo(self, objeto_carta):
        if objeto_carta in self.coleccion and objeto_carta not in self.mazo and len(self.mazo) < 5:
            self.coleccion.remove(objeto_carta)
            self.mazo.append(objeto_carta)
            return True
        #esto agrega a los espiritus/barbaros/duendes que fueron creados por estructuras pero tiene que tener espacio en el mazo
        elif objeto_carta not in self.coleccion and objeto_carta not in self.mazo and len(self.mazo) < 5: 
            self.mazo.append(objeto_carta)
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
    
    def __str__(self): #al final creo que esto no lo uso nunca pero lo hice pq lo pedia el enunciado 
        lineas = []
        lineas.append(f"Jugador - {self.nombre_jugador} | Tienes: {self.oro_disponible}G")

        lineas.append("\nCartas en colección:")
        if len(self.coleccion) == 0:
            lineas.append("sin cartas en colección")
        else:
            indice = 0
            while indice < len(self.coleccion):
                i = self.coleccion[indice]
                linea_carta = f"{i.nombre_carta} | {i.tipo_carta} | Vida: {i.vida_actual}/{i.vida_maxima}"
                lineas.append(f"({indice + 1}) {linea_carta}")
                indice += 1

        lineas.append("\nCartas en mazo:")
        if len(self.mazo) == 0:
            lineas.append("sin cartas en mazo")
        else:
            indice = 0
            while indice < len(self.mazo):
                i = self.mazo[indice]
                linea_carta = f"{i.nombre_carta} | {i.tipo_carta} | Vida: {i.vida_actual}/{i.vida_maxima}"
                lineas.append(f"({indice + 1}) {linea_carta}")
                indice += 1

        return "\n".join(lineas)
