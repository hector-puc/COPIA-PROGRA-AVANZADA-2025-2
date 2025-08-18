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


# PARA MODIFICAR LA CASILLA:

        for i in range(filas + 1):
            cada_fila = []
            for j in range(columnas + 1):
                casilla = self.tablero[i][j]
                if casilla == ".":
                    valor = None
                else:
                    valor = int(casilla)

                if i < filas and j < columnas:
                    cada_fila.append({"valor": valor, "habilitada": True})
                else:
                    cada_fila.append(valor)
            
            self.diccionario.append(cada_fila)
        
        self.diccionario_original = copy.deepcopy(self.diccionario)

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
    
        casilla = self.diccionario[filas][columnas]
        
        if not isinstance(casilla, dict):
            return False
        
        if casilla["valor"] is None:
            return False

        habilitado = not casilla["habilitada"]
        casilla["habilitada"] = habilitado
        
        valor = casilla["valor"]

        
        if habilitado:
            self.tablero[filas][columnas] = str(valor)
        else:
            self.tablero[filas][columnas] = "X" + str(valor)
        
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