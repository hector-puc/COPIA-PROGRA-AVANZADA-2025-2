import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QVBoxLayout, QWidget, QGridLayout, QLineEdit
from PyQt5 import QtWidgets 
from PyQt5.QtCore import Qt

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 100, 300, 300)
        self.setWindowTitle('Ventana Principal')
        self.layout = QVBoxLayout()

        #boton

        self.bienvenda_texto = QLabel('Bienvenido al Departamento de las Colecciones del Cosmos!')
        self.grilla = QVBoxLayout()
        self.boton = QPushButton("Ingresar al Sistema", self)
        self.boton.clicked.connect(self.abrir_ventana_cerrar_actual)
        self.grilla.addWidget(self.boton)
        self.setLayout(self.grilla)
        self.grilla.addWidget(self.bienvenda_texto)
        self.setWindowTitle('Ventana DCC')
    
    
    def abrir_ventana_cerrar_actual(self) -> None:
        self.ventana_ingreso = IngresarSistema()
        self.ventana_ingreso.show()
        self.close()  
    

class IngresarSistema(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 100, 600, 400)
        self.setWindowTitle('Ingreso al Sistema')
        self.grilla = QVBoxLayout()
        etiqueta = QLabel('Panel Principal del DCC!')

        boton_volver = QPushButton("Volver")
        boton_volver.clicked.connect(self.volver_a_principal)
        
        layout_vertical = QVBoxLayout()
        layout_vertical.addWidget(self.seccion_consultas_vbox())
        layout_vertical.addWidget(etiqueta)
        layout_vertical.addWidget(boton_volver)
        self.setLayout(layout_vertical)

    def volver_a_principal(self) -> None:
        
        self.ventana_principal = VentanaPrincipal()
        self.ventana_principal.show()
        self.close()
    
    def abrir_ventana_resultado(self) -> None:
        self.ventana_resultado = VentanaResultado()
        self.ventana_resultado.show()

    def abrir_ventana_csv(self) -> None:
        self.ventana_csv = VentanaRutaCSV()
        self.ventana_csv.show()

    def seccion_consultas_vbox(self) -> QtWidgets.QGroupBox:
        grupo_consultas = QtWidgets.QGroupBox("Consultas")

        layout_vertical_botones = QtWidgets.QVBoxLayout()
        nombres_botones_consulta = (
            "Disponibilidad por planeta",
            "Naves por intervalo de carga",
            "Misiones desde fecha",
            "Planetas por estadísticas",
            "Ganancias potenciales por planeta",
            "Planetas visitados por nave",
            "Mineral por nave",
            "Porcentaje de extracción",)

        for nombre_boton in nombres_botones_consulta:
            boton_consulta = QtWidgets.QPushButton(nombre_boton)
            layout_vertical_botones.addWidget(boton_consulta)
        
        boton_abrir_resultado = QPushButton("Abrir Ventana Resultado")
        boton_abrir_csv = QPushButton("Abrir Ventana CSV")
        boton_abrir_resultado.clicked.connect(self.abrir_ventana_resultado)
        boton_abrir_csv.clicked.connect(self.abrir_ventana_csv)
        layout_vertical_botones.addWidget(boton_abrir_resultado)
        layout_vertical_botones.addWidget(boton_abrir_csv)

        grupo_consultas.setLayout(layout_vertical_botones)
        return grupo_consultas

        

    def cargar_archivo_csv(self):
        pass

    def seccion_consultas(self):
        pass

    def seccion_resultados_con_scroll(self):
        pass

class VentanaRutaCSV(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ruta CSV")
        self.setGeometry(300, 100, 400, 200)

        layout_vertical_principal = QVBoxLayout(self)

        etiqueta = QLabel("Ruta del archivo CSV:", self)
        self.campo_ruta_archivo_csv = QLineEdit(self)
        self.campo_ruta_archivo_csv.setPlaceholderText("Escribe o pega aquí la ruta del CSV")

        layout_vertical_principal.addWidget(etiqueta)
        layout_vertical_principal.addWidget(self.campo_ruta_archivo_csv)

class VentanaResultado(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Resultado:")
        self.setGeometry(300, 100, 400, 200)


        layout_vertical_principal = QVBoxLayout(self)
        etiqueta_resultado = QLabel("Resultado", self)

        layout_vertical_principal.addWidget(etiqueta_resultado)

if __name__ == '__main__':
    def hook(type, value, traceback) -> None:
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = QtWidgets.QApplication([])
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())