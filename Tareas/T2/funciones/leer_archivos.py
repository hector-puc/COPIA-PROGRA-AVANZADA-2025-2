import os

def leer_csv_como_lista(ruta_csv):
    lista_de_filas = []

    with open(ruta_csv, "r", encoding="utf-8") as archivo_csv:

        #para saber si era el encabezado = https://www.freecodecamp.org/espanol/news/enumerar-en-python-ejemplo-de-enumeracion-de-python-para-indice-de-bucle
        for linea_0, linea in enumerate(archivo_csv):
            linea_limpia = linea.strip()

            if not linea_limpia:
                continue
        
            fila = linea_limpia.split(",")

            if linea_0 == 0:
                encabezado = fila
                continue
            
            lista_de_filas.append(fila)

    return encabezado, lista_de_filas

def lista_csv_a_diccionario(ruta_csv):
    lineas_iniciales = leer_csv_como_lista(ruta_csv)

    if not lineas_iniciales:
        return []
    
    lista_encabezados, lista_de_filas = leer_csv_como_lista(ruta_csv)
    
    lista_diccionarios = []

    for lineas_datos in lista_de_filas:
        
        diccionario_fila = {}
        for i in range(len(lista_encabezados)):
            clave = lista_encabezados[i]
            valor = lineas_datos[i]

            diccionario_fila[clave] = valor
    
        lista_diccionarios.append(diccionario_fila) # puede faltar una indentacion
    
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



        
