import sys
from PyQt5 import QtWidgets
from Preparcial import Ui_MainWindow # importa nuestro archivo generado
import sqlite3
from sqlite3 import Error

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self) # inicializar el mywindow

        try:
            self.MiCon = sqlite3.connect("Base_Preparcial.db")
            self.CursorObj = self.MiCon.cursor()
        except Error:
            print(Error) #la conexion con la base de datos 

        try:
            self.CursorObj.execute("Create Table Ciclista(Nombre text, Apellido text, Numero_inscripcion integer, Cedula integer, Fecha_Nacimiento integer, Pais_Origen integer, Numero_equipo integer, Ranking_UCI integer)")
            self.MiCon.commit()# se crea los items de la tabla
        except: self.MiCon.commit()

        #conexion de los botones y los metodos
        
        self.ui.Boton_agregar.clicked.connect(self.Agregar_a_la_Base)
        self.ui.Boton_consultar.clicked.connect(self.Consultar_base)
        self.ui.Boton_borrar.clicked.connect(self.Borrar_ciclista)
        self.ui.Boton_cambiar_nacionalidad.clicked.connect(self.cambiar_nacionalidad)
        self.ui.Salir.clicked.connect(self.Salir)

    def Agregar_a_la_Base(self):
        self.Nombre_texto=self.ui.tx_Nombre.text()
        self.Apellido_texto = self.ui.tx_Apellido.text()
        self.Numero_texto = self.ui.tx_Numero_inscripcion.text()
        self.Cedula_texto = self.ui.tx_Cedula.text()
        self.Fecha_texto = self.ui.tx_Fecha_nacimiento.text()
        self.Pais_texto = self.ui.tx_Pais_origen.text()
        self.Equipo_texto = self.ui.tx_Numero_equipo.text()
        self.Ranking_texto = self.ui.tx_Ranquing_UCI.text()

        
        if self.Nombre_texto=="" or self.Apellido_texto=="" or self.Numero_texto=="" or self.Cedula_texto=="" or self.Fecha_texto=="" or self.Pais_texto=="" or self.Equipo_texto=="" or self.Ranking_texto=="" :
            mensaje=QtWidgets.QMessageBox() #abre una ventana
            mensaje.setIcon(QtWidgets.QMessageBox.Information)
            mensaje.setText("No estan llenos todos los campos")
            mensaje.setWindowTitle("Advertencia")
            mensaje.exec_()
        else:
            self.Persona=(self.Nombre_texto,self.Apellido_texto,self.Numero_texto,self.Cedula_texto,self.Fecha_texto,self.Pais_texto,self.Equipo_texto,self.Ranking_texto)
            try: self.CursorObj.execute('''INSERT INTO Ciclista VALUES(?,?,?,?,?,?,?,?)''', self.Persona) #inseta los valores a la tabla
            except Error: exit()
            self.MiCon.commit()

            #limpiar los espacios luego de ejecutar
            
            self.ui.tx_Nombre.clear()
            self.ui.tx_Apellido.clear()
            self.ui.tx_Numero_inscripcion.clear()
            self.ui.tx_Cedula.clear()
            self.ui.tx_Fecha_nacimiento.clear()
            self.ui.tx_Pais_origen.clear()
            self.ui.tx_Numero_equipo.clear()
            self.ui.tx_Ranquing_UCI.clear()

            mensaje = QtWidgets.QMessageBox()
            mensaje.setIcon(QtWidgets.QMessageBox.Information)
            mensaje.setText("El ciclista se ha agregado")
            mensaje.setWindowTitle("Advertencia")
            mensaje.exec_()

    def Consultar_base(self):
        self.orden=self.ui.Escoger_orden.currentText()

        #ordenar la tabla por cualquier item
        
        if self.orden == "Nombre":
            self.consultar="SELECT * FROM Ciclista ORDER BY Nombre ASC"
        elif self.orden == "Apellido":
            self.consultar="SELECT * FROM Ciclista ORDER BY Apellido ASC"
        elif self.orden == "Num inscripcion":
            self.consultar="SELECT * FROM Ciclista ORDER BY Numero_inscripcion ASC"
        elif self.orden == "Cedula":
            self.consultar="SELECT * FROM Ciclista ORDER BY Cedula ASC"
        elif self.orden == "Fecha nacimiento":
            self.consultar="SELECT * FROM Ciclista ORDER BY Fecha_Nacimiento ASC"
        elif self.orden == "Pais origen":
            self.consultar="SELECT * FROM Ciclista ORDER BY Pais_Origen ASC"
        elif self.orden == "Num equipo":
            self.consultar="SELECT * FROM Ciclista ORDER BY Numero_equipo ASC"
        else:
            self.consultar="SELECT * FROM Ciclista ORDER BY Ranking_UCI ASC"

        self.CursorObj.execute(self.consultar)
        self.Filas = self.CursorObj.fetchall()
        

        #se imprimen los valores en la tabla
        self.ui.Tabla.setRowCount(len(self.Filas))
        cont=0
        for row in self.Filas:
            self.ui.Tabla.setItem(cont, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.ui.Tabla.setItem(cont, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.ui.Tabla.setItem(cont, 2, QtWidgets.QTableWidgetItem(str(row[2])))
            self.ui.Tabla.setItem(cont, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            self.ui.Tabla.setItem(cont, 4, QtWidgets.QTableWidgetItem(row[4]))
            self.ui.Tabla.setItem(cont, 5, QtWidgets.QTableWidgetItem(row[5]))
            self.ui.Tabla.setItem(cont, 6, QtWidgets.QTableWidgetItem(str(row[6])))
            self.ui.Tabla.setItem(cont, 7, QtWidgets.QTableWidgetItem(str(row[7])))  
            cont+=1
               
    def Borrar_ciclista(self):
        self.Numero_borrar_texto = self.ui.Num_ciclista_borrar.text()
        if self.Numero_borrar_texto=="":
            mensaje=QtWidgets.QMessageBox()
            mensaje.setIcon(QtWidgets.QMessageBox.Information)
            mensaje.setText("El campo esta vacio")
            mensaje.setWindowTitle("Advertencia")
            mensaje.exec_()
        else:
            self.borrar_info = "DELETE FROM Ciclista Where Numero_inscripcion=(?)" #borra el ciclista dependiendo de el num.inscripcion
            self.CursorObj.execute(self.borrar_info, (self.Numero_borrar_texto,))
            self.MiCon.commit()

            #limpia el lineedit
            self.ui.Num_ciclista_borrar.clear()

            mensaje = QtWidgets.QMessageBox() #abre una ventana 
            mensaje.setIcon(QtWidgets.QMessageBox.Information)
            mensaje.setText("El ciclista se ha eliminado")
            mensaje.setWindowTitle("Advertencia")
            mensaje.exec_()

    def cambiar_nacionalidad(self):
        self.Numero_Cambio_texto = self.ui.Num_ciclista_cambio.text()
        self.Nacionalidad_Cambio_texto = self.ui.Nueva_nacionalidad.text()
        if self.Numero_Cambio_texto == "" or self.Nacionalidad_Cambio_texto == "":
            mensaje = QtWidgets.QMessageBox()
            mensaje.setIcon(QtWidgets.QMessageBox.Information)
            mensaje.setText("No estan todos los campos llenos")
            mensaje.setWindowTitle("Advertencia")
            mensaje.exec_()
        else:
            self.cambiar_info = "UPDATE Ciclista SET Pais_Origen='" + self.Nacionalidad_Cambio_texto + "' Where Numero_inscripcion=(?)" #actualiza el pais del ciclista
            self.CursorObj.execute(self.cambiar_info, (self.Numero_Cambio_texto,))
            self.MiCon.commit()

            self.ui.Num_ciclista_cambio.clear()
            self.ui.Nueva_nacionalidad.clear()

            mensaje = QtWidgets.QMessageBox()
            mensaje.setIcon(QtWidgets.QMessageBox.Information)
            mensaje.setText("La nacionalidad ha sido actualizada")
            mensaje.setWindowTitle("Advertencia")
            mensaje.exec_()

    def Salir(self):
        exit()
app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec())
