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
            yield Mision(int(id_mision),
                         fecha, 
                         hora,
                         int(id_equipo),
                         int(id_planeta),
                         lograda)
            


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


def misiones_desde_fecha(generador_misiones: Generator[Mision, None, None], 
                         fecha: str, inverso: bool) -> Generator[Mision, None, None]:
    if not inverso:
        for adelante in generador_misiones:
            if adelante.fecha >= fecha:
                yield adelante
    else:
        for atras in generador_misiones:
            if atras.fecha <= fecha:
                yield atras


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

    diccionario_patente_a_ids_filtrados = reduce(
        lambda acumulador_patente_a_ids, tripulacion: (acumulador_patente_a_ids[tripulacion.patente],  
            acumulador_patente_a_ids[tripulacion.patente].append(tripulacion.id_astronauta)
                if tripulacion.rango >= rango else None, ) and acumulador_patente_a_ids, 
                generador_tripulacion, defaultdict(list))  #con esto no explota si no existe 

    condicion_minima_cantidad = ((lambda lista_ids_filtrados: True) if minimo_astronautas < 1 
                                 else (lambda lista_ids_filtrados: len(lista_ids_filtrados) 
                                       >= minimo_astronautas))

    for patente, lista_ids_filtrados in diccionario_patente_a_ids_filtrados.items():
        if condicion_minima_cantidad(lista_ids_filtrados):
            yield (patente, (id_astronauta for id_astronauta in lista_ids_filtrados))


def cambiar_rango_astronauta(
        generador_tripulacion: Generator[Tripulacion, None, None], 
        id_astronauta: int, rango_astronauta: int
        ) -> Generator[Tripulacion, None, None]:
    pass


def encontrar_planetas_cercanos(generador_planetas: Generator[Planeta, None, None], x1: int, 
                                y1: int, x2: int, y2: int, cantidad: int | None = None
                                ) -> Generator[Planeta, None, None]:
    pass
 

# Consultas 2 generadores

def disponibilidad_por_planeta(generador_planeta_mineral: Generator[PlanetaMineral, None, None],
                               generador_planetas: Generator[Planeta, None, None], id_mineral: int
                               ) -> Generator[Tuple[str, int, float], None, None]:
    pass


def misiones_por_tipo_planeta(generador_misiones: Generator[Mision, None, None],
                              generador_planetas: Generator[Planeta, None, None], tipo: str
                              ) -> Generator[Mision, None, None]:
    pass


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
