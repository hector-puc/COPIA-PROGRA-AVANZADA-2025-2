from functools import reduce
from itertools import product
from typing import Generator

from utilidades import Pelicula, Genero


# ----------------------------------------------------------------------------
# Parte I: Cargar dataset
# ----------------------------------------------------------------------------

def cargar_peliculas(ruta: str) -> Generator:
    with open(ruta, 'r', encoding='utf-8') as archivo:
        next(archivo)
        for linea in archivo:
            linea = linea.strip().split(',')
            yield Pelicula(int(linea[0]), str(linea[1]), str(linea[2]), int(linea[3]), float(linea[4]))


# ----------------------------------------------------------------------------
# Parte II: Consultas sobre generadores
# ----------------------------------------------------------------------------


def obtener_directores(generador_peliculas: Generator) -> Generator:
    """
    Retorna un generador con el nombre de todos los directores.
    """


    return map(lambda Pelicula: Pelicula.director, generador_peliculas)


def obtener_str_titulos(generador_peliculas: Generator) -> str:
    """
    Genera un str con todos los títulos de las películas separados por ", ".
    """
    titulos = reduce(lambda string, pelicula2: f'{string}, {pelicula2.titulo}', generador_peliculas, '')
    return titulos[2:]


def filtrar_peliculas(
    generador_peliculas: Generator,
    director: str | None = None,
    rating_min: float | None = None,
    rating_max: float | None = None,
) -> filter:
    """
    Filtra los elementos del generador de Películas según lo indicado en el input.
    """
    if director:
        generador_peliculas = filter(lambda pelicula: pelicula.director == director, generador_peliculas)
    if rating_min:
        generador_peliculas = filter(lambda pelicula: pelicula.rating >= rating_min, generador_peliculas)
    if rating_max:
        generador_peliculas = filter(lambda pelicula: pelicula.rating <= rating_max, generador_peliculas)
    return generador_peliculas
    

def filtrar_titulos(
    generador_peliculas: Generator,
    director: str,
    rating_min: float,
    rating_max: float
) -> Generator:
    """
    Genera un str con todos los títulos de las películas separados
    por ", ". Solo se consideran las películas que tengan el mismo
    director que el indicado, tengan un rating igual o mayor al
    rating_min y un rating igual o menor al rating_max.
    """
    return "COMPLETAR"


def filtrar_peliculas_por_genero(
    generador_peliculas: Generator,
    generador_generos: Generator,
    genero: str | None = None,
) -> Generator:
    """
    Crea un generador con todas las combinaciones posibles entre
    el generador de películas y el generador de géneros.
    Después, filtra las pares obtenidos y mantiene únicamente
    los que presentan el mismo id de película.
    Finalmente, retorna una lista con todos los pares pertenecientes
    a la categoría indicada.
    """
    return "COMPLETAR"
