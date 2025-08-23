import os
import tablero

class DCCasillas:

    def __init__(self, usuario:str, config:str) -> None:
        self. usuario = usuario
        self.puntaje = 0
        self.config = config
        self.tablero_actual =  None
        self.tableros = []

        ruta = os.path.join("config", config)
        archivo = open(ruta, "r", encoding="utf-8")
        tablero_info = archivo.readlines()
        archivo.close()

        self.total_tableros =  int(tablero_info[0].strip())

        if not tablero_info:
            return 
        
        archivos_tablero = []
        primer = tablero_info[0].strip().split()
        if primer[0].isdigit():
            cantidad = int(primer[0])
            archivos_tablero = tablero_info[1 : cantidad + 1]
        else:
            archivos_tablero = tablero_info

        for nombre in archivos_tablero:
            nombre = nombre.strip()

            tablero_obj = tablero.Tablero()
            tablero_obj.cargar_tablero(nombre)
            self.tableros.append(tablero_obj)

    def abrir_tablero(self, num_tablero:int) -> None:
        
        if 0 <= num_tablero < len(self.tableros):
            self.tablero_actual = num_tablero
        else:
            pass

    def guardar_estado(self) -> bool: 

        # CREAR ARCHIVO https://www.pythontutorial.net/python-basics/python-create-text-file

        if not isinstance(self.usuario, str) or not self.usuario.strip(): #sin usuario
            return False
        
        if not isinstance(self.tableros, list) or len(self.tableros) == 0: # sin tablero
            return False
    
        carpeta = "data"
        nombre = f"{self.usuario}.txt"
        ruta_archivo = os.path.join(carpeta, nombre)
        
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:

            print(len(self.tableros), file = archivo)
            
            for tablero in self.tableros:
                print(tablero.movimientos, file = archivo)
                print(tablero.filas, tablero.columnas, file = archivo)

                for fila in tablero.tablero:
                    print(" ".join(fila), file = archivo)
        return True
    
        
# PATH https://stackoverflow.com/questions/2259382/pythonic-way-to-check-if-a-file-exists
 
    def recuperar_estado(self) -> bool:

        path = os.path.join("data", f"{self.usuario}.txt")

        if not os.path.exists(path):
            return False
        

        nombre = f"{self.usuario}.txt"
        ruta_archivo = os.path.join(path) #cambie esta linea de (path, nombre) a (path), en casod de error
        
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:

            print(len(self.tableros))
            
            for tablero in self.tableros:
                print(tablero.movimientos)
                print(tablero.filas, tablero.columnas)

                for fila in tablero.tablero:
                    print(" ".join(fila))
        return True
    
