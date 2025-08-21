import collections
from os.path import join
from utilidades import Anime  # IMPORTANT: Debes utilizar esta nametupled


#####################################
#       Parte I - Cargar datos      #
#####################################
def cargar_animes(ruta_archivo: str) -> list:
    with open(ruta_archivo, 'r', encoding='utf-8') as lista:
        ListaAnime = lista.readlines()
        carga = []
        for i in ListaAnime:
            linea = i.strip()
            datos = linea.split(',')
            nombre, capitulos, puntaje, estreno, estudio, *generos = datos
            generos = set(generos[0].split(";"))
            desarrollo = Anime(
                nombre = str(nombre),
                capitulos = int(capitulos),
                puntaje = int(puntaje),
                estreno = int(estreno),
                estudio = str(estudio),
                generos = generos
            )
            carga.append(desarrollo)
        return carga
    



#####################################
#        Parte II - Consultas       #
#####################################
def animes_por_estreno(animes: list) -> dict:
    animes_estreno = {}
    for i in animes:
        anho = i.estreno
        if anho not in animes_estreno:
            animes_estreno[anho] = [i.nombre]
        else:
            animes_estreno[anho].append(i.nombre)

    return animes_estreno


def descartar_animes(generos_descartados: set, animes: list) -> list:
    sin_descartar = []
    for i in animes:
        if not i.generos.intersection(generos_descartados):
            sin_descartar.append(i.nombre)
    return sin_descartar


def resumen_animes_por_ver(*animes: Anime) -> dict:
    if not animes:
        return {
            'puntaje promedio': 0.0,
            'capitulos total' : 0,
            'generos' :set()
        }
    return


def estudios_con_genero(genero: str, **estudios: dict) -> list:
    # TODO: Completar
    return


if __name__ == "__main__":
    #####################################
    #       Parte I - Cargar datos      #
    #####################################
    animes = cargar_animes(join("data", "ejemplo.chan"))
    indice = 0
    for anime in animes:
        print(f"{indice} - {anime}")
        indice += 1

    #####################################
    #        Parte II - Consultas       #
    #####################################
    # Solo se usará los 2 animes del enunciado.
    datos = [
        Anime(
            nombre="Hunter x Hunter",
            capitulos=62,
            puntaje=9,
            estreno=1999,
            estudio="Nippon Animation",
            generos={"Aventura", "Comedia", "Shonen", "Acción"},
        ),
        Anime(
            nombre="Sakura Card Captor",
            capitulos=70,
            puntaje=10,
            estreno=1998,
            estudio="Madhouse",
            generos={"Shoujo", "Comedia", "Romance", "Acción"},
        ),
    ]

    # animes_por_estreno
    estrenos = animes_por_estreno(datos)
    print(estrenos)

    # descartar_animes
    animes = descartar_animes({"Comedia", "Horror"}, datos)
    print(animes)

    # resumen_animes_por_ver
    resumen = resumen_animes_por_ver(datos[0], datos[1])
    print(resumen)

    # estudios_con_genero
    estudios = estudios_con_genero(
        "Shonen",
        Nippon_Animation=[datos[0]],
        Madhouse=[datos[1]],
    )
    print(estudios)
