from funciones.carta import Carta
from funciones.tropa import Tropa
from parametros import DANO_BOMBA, CANNON_ABILITY, CANNON_DECREASE, DIE_PROB, PROB_LAPIDA
from funciones.leer_archivos import cargar_cartas 


def crear_espiritu_igneo(): #busca en el csv y crea al espiritu
    filas_cartas = cargar_cartas()
    for cartas in filas_cartas:
        nombre_en_archivo = str(cartas["nombre"]).strip().lower()
        if nombre_en_archivo == "espíritu ígneo" or nombre_en_archivo == "espiritu igneo":
            nombre_carta = str(cartas["nombre"]).strip()
            tipo_carta = "tropa"
            vida_maxima = int(cartas["vida_maxima"])
            multiplicador_defensa = float(cartas["multiplicador_defensa"])
            precio_carta = int(cartas["precio"])
            probabilidad_especial = float(cartas["probabilidad_especial"])
            ataque_base = int(cartas["ataque"])
            multiplicador_ataque = float(cartas["multiplicador_ataque"])
            descripcion_habilidad = str(cartas["descripcion_habilidad"])
            return Tropa(nombre_carta = nombre_carta, tipo_carta = tipo_carta, vida_maxima = vida_maxima, multiplicador_defensa = multiplicador_defensa, precio_carta = precio_carta, probabilidad_especial = probabilidad_especial, ataque_base = ataque_base, multiplicador_ataque = multiplicador_ataque, habilidad_especial = descripcion_habilidad )
    return None


class Estructura(Carta):

    def __init__(self, nombre_carta: str, tipo_carta: str, vida_maxima: int, multiplicador_defensa: float, precio_carta: int, probabilidad_especial: float, ataque_base: int, multiplicador_ataque: float, habilidad_especial: str):

        super().__init__(nombre_carta, tipo_carta, vida_maxima, multiplicador_defensa, precio_carta, probabilidad_especial)

        self.ataque = 0
        self.multiplicador_ataque = 0.0

        #para restaurar
        self._respaldo_canon = None 
        self.reemplazo_pendiente = False  #recolector u Horno

    def usar_habilidad_especial(self):
        print(f"{self.nombre_carta} intenta usar su habilidad especial.")

    def __str__(self) -> str:
        return (f"{self.nombre_carta} (estructura) - "
                f"Vida: {self.vida_actual}/{self.vida_maxima}, "
                f"Multiplicador Defensa: x{self.multiplicador_defensa}")
    
    def inicio_de_ronda(self, contexto):
        #cañon
        nombre_normal = self.nombre_carta.strip().lower()
        if nombre_normal == "cañón" or nombre_normal == "canon":
            ia = contexto.instancia_ia

            valor_def_tropa_original = ia.multiplicadores_defensa["tropa"]
            valor_def_mixta_original = ia.multiplicadores_defensa["mixta"]
            mi_defensa_original = self.multiplicador_defensa

            ia.multiplicadores_defensa["tropa"] = max(0.0, valor_def_tropa_original - CANNON_ABILITY) #para que no de valores bajo 0
            ia.multiplicadores_defensa["mixta"] = max(0.0, valor_def_mixta_original - CANNON_ABILITY) #same
            self.multiplicador_defensa = mi_defensa_original + CANNON_DECREASE

            self._respaldo_canon = {"defensa_tropa": valor_def_tropa_original, "defensa_mixta": valor_def_mixta_original, "mi_defensa": mi_defensa_original }

            contexto.registro_eventos.append("Gracias al Cañon la IA más vulnerable y defensa del cañon aumentada solo por esta ronda")

    def antes_de_ataque_del_jugador(self, contexto):
        #torre die
        nombre_normal = self.nombre_carta.strip().lower()
        if nombre_normal in ("torre die", "torre ide"):
            if contexto.orden_ataca_primero == "jugador":
                if contexto.generador_aleatorio() < DIE_PROB:
                    contexto.instancia_ia._inhabilitada_esta_ronda = True
                    contexto.registro_eventos.append("La Torre die desahibilitó a la IA esta ronda.")

    def antes_de_recibir_dano(self, contexto) -> bool:
        nombre_normal = self.nombre_carta.strip().lower()
        if nombre_normal == "lapida":
            if contexto.generador_aleatorio() < PROB_LAPIDA:
                contexto.registro_eventos.append("La lapida evitó el daño.")
                return True
        return False

    def morir(self, contexto):
        nombre_normal = self.nombre_carta.strip().lower()

        #recolector de Agua
        if nombre_normal == "recolector de agua":
            if contexto.orden_ataca_primero == "ia":
                nueva_tropa = contexto.instancia_jugador.obtener_tropa_aleatoria_de_coleccion()
                if nueva_tropa:
                    contexto.instancia_jugador.agregar_al_mazo(nueva_tropa)
                    contexto.registro_eventos.append(f"Por la muerte del recolector entra: {nueva_tropa.nombre_carta} de inmediato.")
            else:
                self.reemplazo_pendiente = "recolector"

        #horno
        elif nombre_normal == "horno":
            espiritu = crear_espiritu_igneo()
            if espiritu:
                if contexto.orden_ataca_primero == "ia":
                    contexto.instancia_jugador.agregar_al_mazo(espiritu)
                    contexto.registro_eventos.append("El horno crea un espiritu igneo")
                else:
                    self.reemplazo_pendiente = espiritu

        #torre Bomba
        elif nombre_normal == "torre bomba":
            contexto.instancia_ia.recibir_dano(DANO_BOMBA, "estructura")
            contexto.registro_eventos.append(f"La torre Bomba hace una explosión que hace {DANO_BOMBA} de daño a la IA.")

    def fin_de_ronda(self, contexto):
        if self.reemplazo_pendiente == "recolector":
            if contexto.instancia_jugador.hay_alguna_carta_viva():
                nueva_tropa = contexto.instancia_jugador.obtener_tropa_aleatoria_de_coleccion()
                if nueva_tropa:
                    contexto.instancia_jugador.agregar_al_mazo(nueva_tropa)
                    contexto.registro_eventos.append(f"El recolector hace que entre: {nueva_tropa.nombre_carta} por victoria o supervivencia.")
            self.reemplazo_pendiente = False

        elif isinstance(self.reemplazo_pendiente, Tropa):
            if contexto.instancia_jugador.hay_alguna_carta_viva():
                contexto.instancia_jugador.agregar_al_mazo(self.reemplazo_pendiente)
                contexto.registro_eventos.append("El horno crea un Espiritu igneo por victoria o supervivencia.")
            self.reemplazo_pendiente = None

        #revertir efectos del cañon
        if self._respaldo_canon is not None:
            ia = contexto.instancia_ia
            ia.multiplicadores_defensa["tropa"] = self._respaldo_canon["defensa_tropa"]
            ia.multiplicadores_defensa["mixta"] = self._respaldo_canon["defensa_mixta"]
            self.multiplicador_defensa = self._respaldo_canon["mi_defensa"]
            self._respaldo_canon = None
