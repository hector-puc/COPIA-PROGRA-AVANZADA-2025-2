from typing import Generator, List, Tuple
from math import pi
from itertools import groupby, tee
from functools import reduce
from collections import defaultdict

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
            patente, material, tamano, capacidadd_astronautas, capacidad_minerales, autonomia = linea.strip().split(',')
            yield Nave(patente, 
                       material, 
                       tamano, 
                       int(capacidadd_astronautas), 
                       float(capacidad_minerales), 
                       float(autonomia))

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
            yield Planeta(int(id_planeta),
                          nombre,
                          float(coordenada_x),
                          float(coordenada_y),
                          tamano,
                          tipo)


def cargar_minerales(path: str) -> Generator[Mineral, None, None]:
    with open(path, "r", encoding='utf-8') as archivo:
        next(archivo)
        for linea in archivo:
            id_mineral, nombre, simbolo_quimico, numero_atomico, masa_atomica = linea.strip().split(',')
            yield Mineral(int(id_mineral),
                            nombre,
                            simbolo_quimico,
                            int(numero_atomico),
                            float(masa_atomica))


def cargar_planeta_minerales(path: str) -> Generator[PlanetaMineral, None, None]:
    with open(path, "r", encoding='utf-8') as archivo:
        next(archivo)
        for linea in archivo:
            id_planeta, id_mineral, cantidad_disponible, pureza = linea.strip().split(',')
            yield PlanetaMineral(int(id_planeta),
                                 int(id_mineral),
                                 float(cantidad_disponible),
                                 float(pureza))


def cargar_mision(path: str) -> Generator[Mision, None, None]:
    with open(path, "r", encoding='utf-8') as archivo:
        next(archivo)
        for linea in archivo:
            id_mision, fecha, hora, id_equipo, id_planeta, lograda = linea.strip().split(',')
            yield Mision(int(id_mision),fecha, hora, int(id_equipo), int(id_planeta), lograda)
            
def cargar_materiales_mision(path: str) -> Generator[MisionMineral, None, None]:
    with open(path, "r", encoding='utf-8') as archivo:
        next(archivo)
        for linea in archivo:
            id_mision, id_mineral, cantidad = linea.strip().split(',')
            yield MisionMineral(int(id_mision),
                                int(id_mineral),
                                float(cantidad))


# Consultas 1 generador

def naves_de_material(generador_naves: Generator[Nave, None, None],
                       material: str) -> Generator[Nave, None, None]:
    for nave in generador_naves:
        if nave.material == material:
            yield nave


def misiones_desde_fecha(generador_misiones: Generator[Mision, None, None], #NO CORRE BIEN POR ALGUNA RAZÓN
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
    diccionario_id_planeta_a_cantidad: dict[int, float], registro_planeta_mineral: PlanetaMineral): 
        
        if registro_planeta_mineral.id_mineral == id_mineral:
            diccionario_id_planeta_a_cantidad[registro_planeta_mineral.id_planeta] = (
                registro_planeta_mineral.cantidad_disponible)
        return diccionario_id_planeta_a_cantidad

    cantidad_planteas = reduce(acumular_planetas, 
                                            generador_planeta_mineral, {})

    tupla_planeta = lambda planeta: (planeta.nombre, planeta.id_planeta, 
                                                   float(cantidad_planteas.get(planeta .id_planeta, 0.0)))
    
    #PARA HACER UN FOR CON UN YIELD https://es.stackoverflow.com/questions/313174/funcionamiento-de-yield-from

    yield from map(tupla_planeta, generador_planetas)



def misiones_por_tipo_planeta(generador_misiones: Generator[Mision, None, None], #no corre bien
                              generador_planetas: Generator[Planeta, None, None], tipo: str
                              ) -> Generator[Mision, None, None]:
    
    generador_filtrado = filter(lambda planeta: planeta.tipo == tipo, generador_planetas)
    ids_planetas_tipo = map(lambda planeta: planeta.id_planeta, generador_filtrado)
    set_ids_planetas_tipo = set(ids_planetas_tipo)

    yield from filter(lambda mision: mision.id_planeta in set_ids_planetas_tipo, generador_misiones)
    

def naves_pueden_llevar(generador_naves: Generator[Nave, None, None], 
                        generador_planeta_mineral: Generator[PlanetaMineral, None, None], 
                        id_planeta: int) -> Generator[tuple[str, int, float], None, None]:
    pass
    

# Consultas 3 generadores

def planetas_por_estadisticas(generador_mineral: Generator[Mineral, None, None],
                              generador_planeta_mineral: Generator[PlanetaMineral, None, None], 
                              generador_planeta: Generator[Planeta, None, None], moles_elemento_min: int, 
                              concentracion_molar_min: int, densidad_min: int
                              ) -> Generator[Planeta, None, None]:
    pass

def ganancias_potenciales_por_planeta(generador_minerales: Generator[Mineral, None, None], 
                                      generador_planeta_mineral: Generator[PlanetaMineral, None, None], 
                                      generador_planetas: Generator[Planeta, None, None], precios: dict
                                      ) -> dict:
    pass


def planetas_visitados_por_nave(generador_planetas: Generator[Planeta, None, None], 
                                generador_misiones: Generator[Mision, None, None], 
                                generador_tripulaciones: Generator[Tripulacion, None, None]
                                ) -> Generator[Tuple[str, str|None, int|None], None, None]:
    pass


def mineral_por_nave(generador_tripulaciones: Generator[Tripulacion, None, None], 
                     generador_misiones: Generator[Mision, None, None], 
                     generador_misiones_mineral: Generator[MisionMineral, None, None]
                     ) -> Generator[Tuple[str, float], None, None]:
    pass


def porcentaje_extraccion(generador_tripulacion: Generator[Tripulacion, None, None],
                           generador_mision_mineral: Generator[MisionMineral, None, None], 
                          generador_planeta_mineral: Generator[PlanetaMineral, None, None],
                            mision : Mision) -> Tuple[float, float]:
    pass


# Consultas 4 generadores

def resultado_mision(mision: Mision, generador_naves: Generator[Nave, None, None], 
                     generador_planeta_mineral: Generator[PlanetaMineral, None, None],
                     generador_tripulaciones: Generator[Tripulacion, None, None], 
                     generador_mision_mineral: Generator[MisionMineral, None, None]) -> Mision:
    pass
