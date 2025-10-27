from typing import Generator, List, Tuple
from math import pi
from itertools import groupby, tee
from functools import reduce
from .consultas_2 import (mineral_por_nave, porcentaje_extraccion, resultado_mision)
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


# Cargas 

def cargar_astronautas(path: str) -> Generator[Astronauta, None, None]:
    with open(path, "r", encoding='utf-8') as archivo:
        next(archivo)
        for linea in archivo:
            id_astronauta, nombre, estado = linea.strip().split(',')
            yield Astronauta(int(id_astronauta), nombre, estado)


def cargar_naves(path: str) -> Generator[Nave, None, None]:
    with open(path, "r", encoding="utf-8") as archivo:
        next(archivo)
        for linea in archivo:
            (patente, material, tamano, capacidadd_astronautas, capacidad_minerales, autonomia
             ) = linea.strip().split(',')
            yield Nave(patente, material, tamano, int(capacidadd_astronautas),
                        float(capacidad_minerales), float(autonomia))

def cargar_tripulaciones(path: str) -> Generator[Tripulacion, None, None]:
    with open(path, "r", encoding='utf-8') as archivo:
        next(archivo)
        for linea in archivo:
            id_equipo, patente, id_astronauta, rango = linea.strip().split(',')
            yield Tripulacion(int(id_equipo), patente, int(id_astronauta), int(rango))


def cargar_planetas(path: str) -> Generator[Planeta, None, None]:
    with open(path, "r", encoding='utf-8') as archivo:
        next(archivo)
        for linea in archivo:
            id_planeta, nombre, coordenada_x, coordenada_y, tamano, tipo = linea.strip().split(',')
            yield Planeta(int(id_planeta), nombre, float(coordenada_x), float(coordenada_y), tamano, tipo)


def cargar_minerales(path: str) -> Generator[Mineral, None, None]:
    with open(path, "r", encoding='utf-8') as archivo:
        next(archivo)
        for linea in archivo:
            id_mineral, nombre, simbolo_quimico, numero_atomico, masa_atomica = linea.strip().split(',')
            yield Mineral(int(id_mineral), nombre, simbolo_quimico, int(numero_atomico), float(masa_atomica))


def cargar_planeta_minerales(path: str) -> Generator[PlanetaMineral, None, None]:
    with open(path, "r", encoding='utf-8') as archivo:
        next(archivo)
        for linea in archivo:
            id_planeta, id_mineral, cantidad_disponible, pureza = linea.strip().split(',')
            yield PlanetaMineral(int(id_planeta),
                                 int(id_mineral), float(cantidad_disponible), float(pureza))


def cargar_mision(path: str) -> Generator[Mision, None, None]:
    with open(path, "r", encoding='utf-8') as archivo:
        next(archivo)
        for linea in archivo:
            id_mision, fecha, hora, id_equipo, id_planeta, lograda = linea.strip().split(',')
            lograda_minuscula = lograda.strip().lower()
            bool_o_none = {'true': True, 'false': False, 'none': None, '': None, } #DEBUG
            valor_lograda = bool_o_none.get(lograda_minuscula, None)  #DEBUG
            yield Mision(int(id_mision), fecha, hora, int(id_equipo), int(id_planeta), valor_lograda)
            
def cargar_materiales_mision(path: str) -> Generator[MisionMineral, None, None]:
    with open(path, "r", encoding='utf-8') as archivo:
        next(archivo)
        for linea in archivo:
            id_mision, id_mineral, cantidad = linea.strip().split(',')
            yield MisionMineral(int(id_mision), int(id_mineral), float(cantidad))


# Consultas 1 generador

def naves_de_material(generador_naves: Generator[Nave, None, None],
                       material: str) -> Generator[Nave, None, None]:
    for nave in generador_naves:
        if nave.material == material:
            yield nave


def misiones_desde_fecha(generador_misiones: Generator[Mision, None, None],
                         fecha: str, inverso: bool) -> Generator[Mision, None, None]:
    def predicado_hacia_adelante(mision: Mision) -> bool:
        return mision.fecha >= fecha

    def predicado_hacia_atras(mision: Mision) -> bool:
        return mision.fecha <= fecha

    predicado_por_fecha = predicado_hacia_atras if inverso else predicado_hacia_adelante
    return filter(predicado_por_fecha, generador_misiones)

def naves_por_intervalo_carga(generador_naves: Generator[Nave, None, None], 
                              cargas: tuple[float, float]) -> Generator[Nave, None, None]:
    for nave in generador_naves:
        if cargas[0] <= nave.capacidad_minerales <= cargas[1]:
            yield nave


def planetas_con_cantidad_de_minerales(generador_planeta_mineral: 
                                       Generator[PlanetaMineral, None, None],
                                        id_mineral: int, cantidad_minima: int) -> List[int]:
    planetas = []
    for planeta in generador_planeta_mineral:
        if planeta.id_mineral == id_mineral and (planeta.cantidad_disponible*planeta.pureza) >= cantidad_minima:
            planetas.append(planeta.id_planeta)
    return planetas


def naves_astronautas_rango(generador_tripulacion: Generator[Tripulacion, None, None], rango: int, 
                            minimo_astronautas: int) -> Generator[Tuple[str, Generator], None, None]:
    def crear_funcion_acumuladora(rango_corte: int):

        def acumular_por_patente(diccionario_patente_a_ids, registro_tripulacion="Tripulacion"):
                patente_actual = registro_tripulacion.patente_nave
                if patente_actual not in diccionario_patente_a_ids:
                    diccionario_patente_a_ids[patente_actual] = []
                if registro_tripulacion.rango >= rango_corte:
                    diccionario_patente_a_ids[patente_actual].append(registro_tripulacion.id_astronauta)

                return diccionario_patente_a_ids #con esto no retorna none

        return acumular_por_patente

    funcion_acumuladora = crear_funcion_acumuladora(rango)

    diccionario_patente_a_ids: dict[str, List[int]] = reduce(funcion_acumuladora,
                                                              generador_tripulacion, {})

    condicion_minima_cantidad = ((lambda lista_ids: True) if minimo_astronautas < 1 
                                 else (lambda lista_ids: len(lista_ids) >= minimo_astronautas))

    for patente, lista_ids in diccionario_patente_a_ids.items():
        if condicion_minima_cantidad(lista_ids):
            yield (patente, (id_astronauta for id_astronauta in lista_ids))

#para hacer esto use: https://stackoverflow.com/questions/2166147/namedtuple-replace-doesnt-work-as-described-in-the-documentation

def cambiar_rango_astronauta(generador_tripulacion: Generator[Tripulacion, None, None], 
        id_astronauta: int, rango_astronauta: int) -> Generator[Tripulacion, None, None]:
    
    for tripulacion_nueva in generador_tripulacion:
        yield ( tripulacion_nueva._replace(rango=rango_astronauta
                                           ) if tripulacion_nueva.id_astronauta == id_astronauta 
                                           else tripulacion_nueva)

def encontrar_planetas_cercanos(generador_planetas: Generator[Planeta, None, None], x1: int, 
                                y1: int, x2: int, y2: int, cantidad: int | None = None
                                ) -> Generator[Planeta, None, None]:
    if cantidad is not None:
        for i in range(cantidad):
            planeta = next(generador_planetas)
            if ((x1 <= planeta.coordenada_x <= x2) and (y1 <= planeta.coordenada_y <= y2)):
                yield planeta
    else:
        for planeta in generador_planetas:
            if ((x1 <= planeta.coordenada_x <= x2) and (y1 <= planeta.coordenada_y <= y2)):
                yield planeta
            
 

# Consultas 2 generadores

#PARA HACER ESTO: https://www.freecodecamp.org/news/lambda-functions-in-python

def disponibilidad_por_planeta(generador_planeta_mineral: Generator[PlanetaMineral, None, None],
                               generador_planetas: Generator[Planeta, None, None], id_mineral: int
                               ) -> Generator[Tuple[str, int, float], None, None]:

    def acumular_planetas(
    diccionario_id_planeta_a_cantidad: dict[int, float], planeta_mineral: PlanetaMineral): 
        
        if planeta_mineral.id_mineral == id_mineral:
            diccionario_id_planeta_a_cantidad[planeta_mineral.id_planeta] = (
                planeta_mineral.cantidad_disponible)
        return diccionario_id_planeta_a_cantidad

    cantidad_planteas = reduce(acumular_planetas, 
                                            generador_planeta_mineral, {})

    tupla_planeta = lambda planeta: (planeta.nombre, planeta.id_planeta, 
                                                   float(cantidad_planteas.get(planeta .id_planeta, 0.0)))
    
    #PARA HACER UN FOR CON UN YIELD https://es.stackoverflow.com/questions/313174/funcionamiento-de-yield-from

    yield from map(tupla_planeta, generador_planetas)



def misiones_por_tipo_planeta(generador_misiones: Generator[Mision, None, None], 
                              generador_planetas: Generator[Planeta, None, None], tipo: str
                              ) -> Generator[Mision, None, None]:
    
    ids_y_tipos = set(map(lambda planeta_filtrado: planeta_filtrado.id_planeta,
                          filter(lambda planeta: planeta.tipo == tipo, generador_planetas), ))

    return filter(lambda i: (i.id_planeta in ids_y_tipos) and (i.lograda is not None),
                   generador_misiones, )
    

def naves_pueden_llevar(generador_naves: Generator[Nave, None, None], 
                        generador_planeta_mineral: Generator[PlanetaMineral, None, None], 
                        id_planeta: int) -> Generator[tuple[str, int, float], None, None]:
    
    registros_minerales = tuple(filter(
        lambda planeta_mineral: planeta_mineral.id_planeta == id_planeta, generador_planeta_mineral))
    
    for registro_nave in generador_naves:
        capacidad = float(registro_nave.capacidad_minerales)
        
        porcentaje = lambda registro: ((registro_nave.patente, registro.id_mineral, 0.0)
            if capacidad <= 0.0 or float(registro.cantidad_disponible) <= 0.0
            else (registro_nave.patente, registro.id_mineral,
                   min(100.0, (capacidad / float(registro.cantidad_disponible)) * 100.0))) #con el min pasa la correctitud

        yield from map(porcentaje, registros_minerales)

# Consultas 3 generadores

def planetas_por_estadisticas(generador_mineral: Generator[Mineral, None, None], 
                              generador_planeta_mineral: Generator[PlanetaMineral, None, None], 
                              generador_planeta: Generator[Planeta, None, None], moles_elemento_min: int, 
                              concentracion_molar_min: int, densidad_min: int
                              ) -> Generator[Planeta, None, None]:
    
    diccionario_minerales = dict(map(lambda mineral: (mineral.id_mineral, mineral), 
                                            generador_mineral))
    diccionario_planetas = dict(
        map(lambda planeta: (planeta.id_planeta, planeta), generador_planeta))

    
    diccionario_volumen_por_planeta = dict(map(lambda lambda_planeta: (
                lambda_planeta[0],          #id planeta
                (4.0 / 3.0) * pi * (        #volumen en km3
                    radio_planeta(lambda_planeta[0],
                    lambda_planeta[1].tamano) ** 3)) #tamaño planeta
                    , diccionario_planetas.items())) #el iterable para q sirva el map

    def estadisticas_planetas_acumulado(diccionario_acumulado, registro_planeta_mineral: PlanetaMineral
        ) -> dict[int, dict[str, object]]:

        id_planeta_actual = registro_planeta_mineral.id_planeta
        id_mineral_actual = registro_planeta_mineral.id_mineral

        if id_planeta_actual not in diccionario_acumulado:
            diccionario_acumulado[id_planeta_actual] = {"masa_total": 0.0, "concentracion_molar": {}}

        minerales_calcular = float(registro_planeta_mineral.cantidad_disponible)
        pureza_decimal = float(registro_planeta_mineral.pureza)

        masa_gramos = minerales_calcular * 1000000.0 #viene en toneladas asi q lo paso a gramos y a float con el.0
        masa_pura_gramos = masa_gramos * pureza_decimal

        mineral_objeto = diccionario_minerales.get(id_mineral_actual)
        masa_atomica_mol = float(mineral_objeto.masa_atomica) if mineral_objeto else 0.0
        moles_actuales = (masa_pura_gramos / masa_atomica_mol) if masa_atomica_mol > 0 else 0.0

        diccionario_acumulado[id_planeta_actual]["masa_total"] = ( #actualzia masa total
            float(diccionario_acumulado[id_planeta_actual]["masa_total"]) + masa_gramos)

        #suma moles del mineral actual
        diccionario_moles_por_mineral = diccionario_acumulado[id_planeta_actual]["concentracion_molar"] 
        diccionario_moles_por_mineral[id_mineral_actual] = (
            diccionario_moles_por_mineral.get(id_mineral_actual, 0.0) + moles_actuales)

        return diccionario_acumulado

    diccionario_estadisticas_por_planeta = reduce(estadisticas_planetas_acumulado, 
                                                  generador_planeta_mineral, {})

    def predicado_planeta_cumple(id_planeta: int) -> bool:
        volumen_km3 = diccionario_volumen_por_planeta.get(id_planeta, 0.0)
        if volumen_km3 == 0.0:
            return False
        
        info_planeta = diccionario_estadisticas_por_planeta.get(id_planeta)
        if info_planeta is None:
            return False

        masa_total = float(info_planeta["masa_total"])  
        densidad_total = masa_total / volumen_km3
        if densidad_total < float(densidad_min):
            return False

        concentracion_molar = info_planeta["concentracion_molar"] 

        def mineral_cumple(moles_elemento: float) -> bool:
            return (moles_elemento >= float(moles_elemento_min)) and \
                   ((moles_elemento / volumen_km3) >= float(concentracion_molar_min))

        return any(map(mineral_cumple, concentracion_molar.values()))

    generador_ids_planeta = (i for i in diccionario_estadisticas_por_planeta.keys())
    yield from map(
        lambda i: diccionario_planetas[i], filter(predicado_planeta_cumple, generador_ids_planeta))

def ganancias_potenciales_por_planeta(generador_minerales: Generator[Mineral, None, None], 
                                      generador_planeta_mineral: Generator[PlanetaMineral, None, None], 
                                      generador_planetas: Generator[Planeta, None, None], precios: dict) -> dict:
    
    diccionario_precio = dict(map(
        lambda mineral: (mineral.id_mineral, float(precios.get(mineral.nombre, 0.0))), generador_minerales))
    diccionario_valor_potencial = dict(map(lambda planeta: (planeta.id_planeta, 0.0), generador_planetas))

    def acumulador_valor_potencial(
        diccionario_acumulado: dict[int, float],
        registro_planeta_mineral: PlanetaMineral) -> dict[int, float]:

        id_planeta_actual = registro_planeta_mineral.id_planeta
        id_mineral_actual = registro_planeta_mineral.id_mineral

        precio_por_tonelada = diccionario_precio.get(id_mineral_actual, 0.0)
        cantidad_pura_toneladas = float(registro_planeta_mineral.cantidad_disponible
                                        ) * float(registro_planeta_mineral.pureza)
        valor_del_mineral_en_este_planeta = precio_por_tonelada * cantidad_pura_toneladas
        diccionario_acumulado[id_planeta_actual] = diccionario_acumulado.get(id_planeta_actual, 0.0
                                                                             ) + valor_del_mineral_en_este_planeta
        
        return diccionario_acumulado

    return reduce(acumulador_valor_potencial, generador_planeta_mineral, diccionario_valor_potencial)


def planetas_visitados_por_nave(generador_planetas: Generator[Planeta, None, None], 
                                generador_misiones: Generator[Mision, None, None], 
                                generador_tripulaciones: Generator[Tripulacion, None, None]
                                ) -> Generator[Tuple[str, str|None, int|None], None, None]:
    diccionario_nombres_planetas_por_id = dict(
        map(lambda planeta: (planeta.id_planeta, planeta.nombre), generador_planetas))

    diccionario_patente_tripulacion = dict(
        map(lambda tripulacion: (tripulacion.id_equipo, tripulacion.patente_nave),
            generador_tripulaciones))
    conjunto_patentes_a_consultar = set(diccionario_patente_tripulacion.values())

    def acumular_planetas_visitados(diccionario_acumulado: dict[str, set[int]],
                                                mision_actual: Mision):
        if (mision_actual.lograda is None) or (mision_actual.id_planeta is None):
            return diccionario_acumulado

        patente_de_mision = diccionario_patente_tripulacion.get(mision_actual.id_equipo)
        if patente_de_mision is None:
            return diccionario_acumulado

        id_planeta_visitado = mision_actual.id_planeta
        if id_planeta_visitado not in diccionario_nombres_planetas_por_id:
            return diccionario_acumulado

        if patente_de_mision not in diccionario_acumulado:
            diccionario_acumulado[patente_de_mision] = set() #asi no lo repito
        diccionario_acumulado[patente_de_mision].add(id_planeta_visitado)

        return diccionario_acumulado

    diccionario_iniciado = dict(
        map(lambda patente: (patente, set()), conjunto_patentes_a_consultar))

    diccionario_planetas_visitados_por_patente = reduce(
        acumular_planetas_visitados, generador_misiones, diccionario_iniciado)

    for patente_nave in sorted(conjunto_patentes_a_consultar):
        conjunto_ids_visitados = diccionario_planetas_visitados_por_patente.get(patente_nave, set())
        if not conjunto_ids_visitados:
            yield (patente_nave, None, None)
        else:
            for id_planeta_visitado in sorted(conjunto_ids_visitados):
                nombre_planeta_visitado = diccionario_nombres_planetas_por_id[id_planeta_visitado]
                yield (patente_nave, nombre_planeta_visitado, id_planeta_visitado)


