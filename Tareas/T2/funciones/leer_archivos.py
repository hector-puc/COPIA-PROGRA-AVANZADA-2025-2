import os

def partir_linea(linea_cruda): #esto es para cuando las descripciones tienen comas
    linea_limpia = linea_cruda.rstrip("\n")

    #nombre, vida_maxima, ataque, resto
    partes_iniciales = linea_limpia.split(",", 3)
    if len(partes_iniciales) < 4:
        return []

    texto_nombre = partes_iniciales[0].strip()
    texto_vida_maxima = partes_iniciales[1].strip()
    texto_ataque = partes_iniciales[2].strip()
    texto_resto = partes_iniciales[3].strip()

    #probabilidad, velocidad
    partes_finales = texto_resto.rsplit(",", 2)
    if len(partes_finales) < 3:
        return []

    texto_descripcion = partes_finales[0].strip()
    texto_probabilidad_especial = partes_finales[1].strip()
    texto_velocidad = partes_finales[2].strip()

    

    return [texto_nombre, texto_vida_maxima, texto_ataque, texto_descripcion, texto_probabilidad_especial, texto_velocidad]

def leer_csv_como_lista(ruta_csv):
    lista_de_filas = []
    encabezado = []
    es_archivo_ia = False

    with open(ruta_csv, "r", encoding="utf-8") as archivo_csv:
        for indice_linea, linea_cruda in enumerate(archivo_csv):
            linea_limpia = linea_cruda.strip()
            if not linea_limpia:
                continue

            if indice_linea == 0:
                encabezado_normalizados = []
                encabezado = []
                for i in linea_limpia.strip().split(","):
                    encabezado.append(i.strip())
                for j in encabezado:
                    encabezado_normalizados.append(j)
                es_archivo_ia = (encabezado_normalizados == ["nombre", "vida_maxima", "ataque", "descripcion", "probabilidad_especial", "velocidad"])
                continue

            if es_archivo_ia:
                #decripcion ia con comas
                fila_valores = partir_linea(linea_limpia)
                if fila_valores and len(fila_valores) == len(encabezado):
                    lista_de_filas.append(fila_valores)
            else:
                maximo_cortes = max(0, len(encabezado) - 1)
                partes = linea_limpia.split(",", maximo_cortes)

                #quitar las comillas
                indice = 0
                while indice < len(partes):
                    campo = partes[indice].strip()
                    if len(campo) >= 2 and campo[0] == '"' and campo[-1] == '"':
                        campo = campo[1:-1].replace('""', '"')
                    partes[indice] = campo
                    indice += 1

                lista_de_filas.append(partes)

    return encabezado, lista_de_filas

def lista_csv_a_diccionario(ruta_csv):
    encabezado, lista_de_filas = leer_csv_como_lista(ruta_csv)
    if not encabezado:
        return []

    lista_diccionarios = []
    for lista_campos in lista_de_filas:
        diccionario_fila = {}
        limite = min(len(encabezado), len(lista_campos))
        indice = 0
        while indice < limite:
            clave = encabezado[indice]
            valor = lista_campos[indice]
            diccionario_fila[clave] = valor
            indice += 1
        lista_diccionarios.append(diccionario_fila)

    return lista_diccionarios


def cargar_cartas():
    ruta = os.path.join("data", "cartas.csv")
    return lista_csv_a_diccionario(ruta)

def cargar_ias(dificultad):
    nombre_archivo_ia = f"ias_{dificultad}.csv"
    ruta = os.path.join("data", nombre_archivo_ia)
    return lista_csv_a_diccionario(ruta)

def cargar_multiplicadores():
    ruta = os.path.join("data", "multiplicadores.csv")
    return lista_csv_a_diccionario(ruta)



        
