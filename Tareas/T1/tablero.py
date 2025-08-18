import os
import visualizador


class Tablero:

    def __init__(self) -> None:
        self.tablero = []
        self.movimientos = 0
        self.estado = False


    def cargar_tablero(self, archivo:str) -> None:
        ruta = os.path.join("config", archivo)

        self.tablero = [] 


        data = open(ruta, "r", encoding="utf-8")
        info = data.readlines()
        data.close()

        dimensiones = info[0].strip().split(" ")
        filas = int(dimensiones[0])
        columnas = int(dimensiones[1])

        for i in range(filas + 1):
            fila = info[i + 1].strip().split()
            self.tablero.append(fila)
        
        #self.tablero.append(fila)


    def mostrar_tablero(self) -> None:
        visualizador.imprimir_tablero(self.tablero)

    def modificar_casilla(self, fila:int, columna:int) -> bool:

        fila = int(fila)
        columna = int(columna)

        if fila < 0 or fila >= len(self.tablero):
            return False
        if columna < 0 or columna >= len(self.tablero[0]):
            return False
    
        casilla = self.tablero[fila][columna]
        
        if not isinstance(casilla, dict):
            return False
        else:
            casilla["habilitada"] = not casilla["habilitada"]
            self.movimientos += 1
            return True
        
    def validar(self) -> bool:
        filas = len(self.tablero) - 1
        columnas = len(self.tablero[0]) - 1

#filas
        for i in range(filas):
            obj = self.tablero[i][columnas]
            if obj is not None:
                suma = 0
                for j in range(columnas):
                    casilla = self.tablero[i][j]
                    if casilla["habilitada"]:
                        suma += casilla["valor"]
                
                if suma != obj:
                    return False

#columnas
        for j in range(columnas):
            obj = self.tablero[filas][j]
            if obj is not None:
                suma = 0
                for i in range(filas):
                    casilla = self.tablero[i][j]
                    if casilla["habilitada"]:
                        suma += casilla["valor"]
                
                if suma != obj:
                    return False
        
        self.estado = True
        return True
    
#BACKTRACKING https://www.geeksforgeeks.org/dsa/introduction-to-backtracking-2

    #def encontrar_solucion(self) -> Tablero:
    #    pass