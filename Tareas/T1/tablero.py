import os
from visualizador import imprimir_tablero
import copy

class Tablero:

    def __init__(self) -> None:
        self.tablero = []
        self.movimientos = 0
        self.estado = False
        self.filas = 0
        self.columnas = 0
        self.diccionario = []
        self.diccionario_original = []

    def cargar_tablero(self, archivo:str) -> None:
        ruta = os.path.join("config", archivo)

        self.tablero = []
        self.diccionario = []
        self.diccionario_original = []
        self.movimientos = 0
        self.estado = False
        

        data = open(ruta, "r", encoding="utf-8")
        info = data.readlines()
        data.close()

        dimensiones = info[0].strip().split()
        filas = int(dimensiones[0])
        columnas = int(dimensiones[1])

        self.filas = filas
        self.columnas = columnas

        #TABLERO ORIGINAL:

        for i in range(filas + 1):
            if i +1 >= len(info):
                break
            original = info[i +1].strip().split(" ")
            self.tablero.append(original)

        #self.diccionario_original = copy.deepcopy(self.diccionario)

    def mostrar_tablero(self) -> None:
        imprimir_tablero(self.tablero)


# TRY, EXCEPT https://docs.python.org/es/3.13/tutorial/errors.html

    def modificar_casilla(self, fila:int, columna:int) -> bool:
        try:
            filas = int(fila)
            columnas = int(columna)
        except ValueError:
            return False
        
        if self.tablero == []:
            return False

        if filas < 0 or filas >= self.filas:
            return False
        if columnas < 0 or columnas >= self.columnas:
            return False
    
        
        casilla = self.tablero[fila][columna].strip()
    
        if isinstance(casilla, str):

            if casilla.startswith("X"):
                self.tablero[filas][columnas] = casilla[1:]
            elif casilla == "." or casilla == "":
                return False
            else:
                self.tablero[filas][columnas] = "X" + casilla
        else:
            self.tablero[filas][columnas] = "X" + str(casilla)

        self.movimientos += 1
        return True


    def validar(self) -> bool:
        
        if not self.tablero or not self.tablero[0]: #si no existe tablero o esta vacio
            self.estado = False
            return False

        
        filas_sin_adicional = len(self.tablero) - 1        
        columnas_sin_adicional = len(self.tablero[0]) - 1     

        
        for i in range(filas_sin_adicional):
            objetivo_str = self.tablero[i][columnas_sin_adicional]
            if objetivo_str != "." and objetivo_str != "":
                try:
                    objetivo = int(objetivo_str)
                except ValueError:
                    self.estado = False
                    return False


                suma = 0
                for j in range(columnas_sin_adicional):
                    casilla = self.tablero[i][j]
                    
                    if casilla == "." or casilla == "" or (isinstance(casilla, str) and casilla.startswith("X")):
                        continue
                    try:
                        suma += int(casilla)
                    except ValueError:
                        self.estado = False
                        return False


                if suma != objetivo:
                    self.estado = False
                    return False

        
        for j in range(columnas_sin_adicional):
            objetivo_str = self.tablero[filas_sin_adicional][j]
            if objetivo_str != "." and objetivo_str != "":

                try:
                    objetivo = int(objetivo_str)
                
                except ValueError:
                    self.estado = False
                    return False

                suma = 0
                for i in range(filas_sin_adicional):
                    casilla = self.tablero[i][j]
                    if casilla == "." or casilla == "" or (isinstance(casilla, str) and casilla.startswith("X")):
                        continue
                    
                    try:
                        suma += int(casilla)
                    
                    except ValueError:
                        self.estado = False
                        return False

                if suma != objetivo:
                    self.estado = False
                    return False

        
        self.estado = True
        return True

#BACKTRACKING https://www.geeksforgeeks.org/dsa/introduction-to-backtracking-2

    def encontrar_solucion(self):
        
        tablero_copia = copy.deepcopy(self.tablero)

        
        posiciones_jugables = []
        
        for i in range(len(tablero_copia) - 1):
            for j in range(len(tablero_copia[0]) - 1):
                if tablero_copia[i][j] != "." and tablero_copia[i][j] != "":
                    posiciones_jugables.append((i, j))
        

        def backtrack(indice_posicion):
            
            if indice_posicion == len(posiciones_jugables):
                
                tablero_temporal = Tablero()
                tablero_temporal.tablero = tablero_copia
                return tablero_temporal.validar()

            fila_actual, columna_actual = posiciones_jugables[indice_posicion]
            valor_original = str(tablero_copia[fila_actual][columna_actual])

            #dejar la casilla igual
            if backtrack(indice_posicion + 1):
                return True

            #desahibilitar
            tablero_copia[fila_actual][columna_actual] = "X" + str(valor_original)

            if backtrack(indice_posicion + 1):
                return True

            #restaurar casilla
            tablero_copia[fila_actual][columna_actual] = valor_original
            return False

        if backtrack(0):
            tablero_resuelto = Tablero()
            tablero_resuelto.tablero = tablero_copia
            return tablero_resuelto
        else:
            return None