import os
import visualizador
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
            original = info[i +1].strip().split(" ")
            self.tablero.append(original)


        #self.diccionario_original = copy.deepcopy(self.diccionario)

    def mostrar_tablero(self) -> None:
        visualizador.imprimir_tablero(self.tablero)


# TRY, EXCEPT https://docs.python.org/es/3.13/tutorial/errors.html

    def modificar_casilla(self, fila:int, columna:int) -> bool:
        try:
            filas = int(fila)
            columnas = int(columna)
        except ValueError:
            return False
        

        if filas < 0 or filas >= self.filas:
            return False
        if columnas < 0 or columnas >= self.columnas:
            return False
    

        if casilla.startswith("X"):
            self.tablero[filas][columnas] = casilla[1:]
        else:
            self.tablero[filas][columnas] = "X" + casilla
        
        self.movimientos += 1


    def validar(self) -> bool:
        # filas
        for i in range(self.filas):
            objetivo = self.tablero[i][self.columnas].strip()
            if objetivo != "." and objetivo != "":
                
                objetivo = int(objetivo)
            
                suma = 0

                for j in range(self.columnas):
                    casilla = self.tablero[i][j].strip()
                    if casilla.startswith("X"):
                        continue
                    if casilla == "." or casilla == "":
                        continue
                    valor_suma = int(casilla)
                    suma += valor_suma
                
                if suma != objetivo:
                    self.estado = False
                    return False

            # columnas
        for j in range(self.columnas):
            objetivo = self.tablero[self.filas][j].strip()
            if objetivo != "." and objetivo != "":
                objetivo = int(objetivo)
            
                suma = 0

                for i in range(self.filas):
                    casilla = self.tablero[i][j].strip()
                    if casilla.startswith("X"):
                        continue
                    if casilla == "." or casilla == "":
                        continue
                    valor_suma = int(casilla)
                    suma += valor_suma
                
                if suma != objetivo:
                    self.estado = False
                    return False
            
        self.estado = True
        return True



#BACKTRACKING https://www.geeksforgeeks.org/dsa/introduction-to-backtracking-2

    #def encontrar_solucion(self) -> Tablero:
    #    pass