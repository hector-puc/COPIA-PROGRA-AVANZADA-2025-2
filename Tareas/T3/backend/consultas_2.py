from typing import Generator, List, Tuple
from math import pi
from itertools import groupby, tee
from functools import reduce

from utilidades import (
    Astronauta,
    Nave,
    Tripulacion,
    Planeta,
    Mineral,
    PlanetaMineral,
    Mision,
    MisionMineral,
    radio_planeta
)


def mineral_por_nave(generador_tripulaciones: Generator[Tripulacion, None, None], 
                     generador_misiones: Generator[Mision, None, None], 
                     generador_misiones_mineral: Generator[MisionMineral, None, None]
                     ) -> Generator[Tuple[str, float], None, None]:
    
    diccionario_gatochico = dict(
        map(lambda registro_tripulacion: (registro_tripulacion.id_equipo, registro_tripulacion.patente_nave), 
            generador_tripulaciones))
    todas_las_patentes = set(diccionario_gatochico.values())

    def acumular_cantidad_mision(diccionario_acumulado, registro_mision_mineral: MisionMineral
                                       ) -> dict[int, float]:
        mision_actual = registro_mision_mineral.id_mision
        cantidad_requerida = float(registro_mision_mineral.cantidad)
        diccionario_acumulado[mision_actual] = (diccionario_acumulado.get(mision_actual, 0.0) + cantidad_requerida)
        return diccionario_acumulado

    diccionario_cantidades_mision = reduce(acumular_cantidad_mision, generador_misiones_mineral, {})

    def acumulador_de_patente(diccionario_totales, registro_mision: Mision) -> dict[str, float]:

        if registro_mision.lograda is not True:
            return diccionario_totales

        patente_asociada = diccionario_gatochico.get(registro_mision.id_equipo)
        if patente_asociada is None:
            return diccionario_totales

        total_mision = float(diccionario_cantidades_mision.get(registro_mision.id_mision, 0.0))
        diccionario_totales[patente_asociada] = (diccionario_totales.get(patente_asociada, 0.0
                                                                         ) + total_mision)
        return diccionario_totales

    diccionario_de_patentes = reduce(acumulador_de_patente, generador_misiones, {})

    return map(
        lambda patente_nave: (patente_nave, float(diccionario_de_patentes.get(patente_nave, 0.0))), 
        sorted(todas_las_patentes))

def porcentaje_extraccion(generador_tripulacion: Generator[Tripulacion, None, None], 
                          generador_mision_mineral: Generator[MisionMineral, None, None], 
                          generador_planeta_mineral: Generator[PlanetaMineral, None, None],
                          mision : Mision) -> Tuple[float, float]:
    if mision.lograda is not True:
        return (0.0, 0.0)

    def totales_y_minerales(acumulado_total_y_conjunto, registro_mision_mineral: MisionMineral):
        
        total_momentaneo, conjunto_ids_minerales = acumulado_total_y_conjunto

        return (total_momentaneo + float(registro_mision_mineral.cantidad),
            conjunto_ids_minerales.union({registro_mision_mineral.id_mineral})
        ) if registro_mision_mineral.id_mision == mision.id_mision else acumulado_total_y_conjunto

    total_puro_por_mision, conjunto_ids_minerales_de_la_mision = reduce(
        totales_y_minerales, generador_mision_mineral, (0.0, set()))

    def cantidad_pura_planeta(total_puro_planeta: float,
        registro_planeta_mineral: PlanetaMineral) -> float:
        coincide_planeta = (registro_planeta_mineral.id_planeta == mision.id_planeta)
        coincide_mineral = (registro_planeta_mineral.id_mineral in conjunto_ids_minerales_de_la_mision)
        return (total_puro_planeta +
            float(registro_planeta_mineral.cantidad_disponible) * float(registro_planeta_mineral.pureza)
        ) if (coincide_planeta and coincide_mineral) else total_puro_planeta

    total_puro_planeta = reduce(cantidad_pura_planeta, generador_planeta_mineral, 0.0)

    porcentaje_total_extraido = (0.0 if total_puro_planeta <= 0.0
        else (total_puro_por_mision / total_puro_planeta) * 100.0)

    cantidad_tripulantes_en_mision = reduce(
        lambda cantidad, registro_trip: cantidad + (1 if registro_trip.id_equipo == mision.id_equipo else 0),
        generador_tripulacion, 0)

    porcentaje_por_tripulante = (0.0 if cantidad_tripulantes_en_mision <= 0
        else porcentaje_total_extraido / float(cantidad_tripulantes_en_mision))

    return (porcentaje_total_extraido, porcentaje_por_tripulante)
    
# Consultas 4 generadores

def resultado_mision(mision: Mision, generador_naves: Generator[Nave, None, None], 
                     generador_planeta_mineral: Generator[PlanetaMineral, None, None],
                     generador_tripulaciones: Generator[Tripulacion, None, None], 
                     generador_mision_mineral: Generator[MisionMineral, None, None]) -> Mision:
    if mision.id_planeta is None:
        return mision._replace(lograda=False)

    def requerimientos(acumulado: dict[int, float], registro: MisionMineral) -> dict[int, float]:
        if registro.id_mision != mision.id_mision:
            return acumulado
        identificador_mineral = registro.id_mineral
        cantidad_pura_requerida = float(registro.cantidad)
        acumulado[identificador_mineral] = acumulado.get(identificador_mineral, 0.0) + cantidad_pura_requerida
        return acumulado

    diccionario_cantidad_pura = reduce(requerimientos, generador_mision_mineral, {})

    #si no estan los minerales la mision falla
    if not diccionario_cantidad_pura:
        return mision._replace(lograda=False)

    conjunto_minerales_pedidos = set(diccionario_cantidad_pura.keys())

    #gatochico id=1
    gatochico = float(diccionario_cantidad_pura.get(1, 0.0))
    if gatochico > 0.0:
        diccionario_gatochico = dict(map(lambda i: (i.id_equipo, i.patente_nave), generador_tripulaciones))
        patente_nave_objetivo = diccionario_gatochico.get(mision.id_equipo)
        if patente_nave_objetivo is None:
            return mision._replace(lograda=False)

        diccionario_capacidad_por_patente = dict(
            map(lambda i: (i.patente, float(i.capacidad_minerales)), generador_naves))
        capacidad_impura_de_nave = diccionario_capacidad_por_patente.get(patente_nave_objetivo)
        if capacidad_impura_de_nave is None:
            return mision._replace(lograda=False)

        mision_lograda = (gatochico <= float(capacidad_impura_de_nave))
        return mision._replace(lograda=bool(mision_lograda))
    
    conjunto_minerales_pedidos = set(diccionario_cantidad_pura.keys())

    def acumulador_planeta(acumulado, registro: PlanetaMineral):
        if (registro.id_planeta == mision.id_planeta) and (
            registro.id_mineral in conjunto_minerales_pedidos):
            acumulado[registro.id_mineral] = (float(registro.cantidad_disponible), float(registro.pureza))
        return acumulado

    diccionario_impuro = reduce(acumulador_planeta, generador_planeta_mineral, {})

    def calcular_impuro(id_y_cantidad_pura) -> float:
        id_mineral, cantidad_pura = id_y_cantidad_pura
        if id_mineral == 1:
            return float(cantidad_pura)
        stock = diccionario_impuro.get(id_mineral)
        if stock is None:
            return False
        cantidad_impura_disponible, pureza_decimal = stock
        if pureza_decimal <= 0.0:
            return False
        impuro_necesario = cantidad_pura / pureza_decimal
        if cantidad_impura_disponible + 0.0 < impuro_necesario:
            return False
        return impuro_necesario

    lista_impuro_necesario = list(
        map(calcular_impuro, diccionario_cantidad_pura.items()))

    if any(map(lambda x: x == False, lista_impuro_necesario)):
        return mision._replace(lograda = False)

    total_impuro_toneladas = sum(lista_impuro_necesario)

    diccionario_gatochico = dict(map(lambda i: (i.id_equipo, i.patente_nave), generador_tripulaciones))
    patente_nave_objetivo = diccionario_gatochico.get(mision.id_equipo)
    if patente_nave_objetivo is None:
        return mision._replace(lograda=False)

    diccionario_capacidad_por_patente = dict(
        map(lambda n: (n.patente, float(n.capacidad_minerales)), generador_naves))
    capacidad_impura_de_nave = diccionario_capacidad_por_patente.get(patente_nave_objetivo)
    
    if capacidad_impura_de_nave is None:
        return mision._replace(lograda=False)

    mision_lograda = (total_impuro_toneladas <= float(capacidad_impura_de_nave))
    return mision._replace(lograda = bool(mision_lograda))