import sys
from PyQt5 import QtWidgets
from UI import Ui_MainWindow
from database import CyclingDatabase


class mywindow(QtWidgets.QMainWindow):
    def __init__(self, db_path: str = "Base_Preparcial.db"):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db = CyclingDatabase(db_path)

        self.ui.Boton_agregar.clicked.connect(self.Agregar_a_la_Base)
        self.ui.Boton_consultar.clicked.connect(self.Consultar_base)
        self.ui.Boton_borrar.clicked.connect(self.Borrar_ciclista)
        self.ui.Boton_cambiar_nacionalidad.clicked.connect(self.cambiar_nacionalidad)
        self.ui.Salir.clicked.connect(self.Salir)

    def _show_message(self, text: str, title: str = "Información") -> None:
        mensaje = QtWidgets.QMessageBox()
        mensaje.setIcon(QtWidgets.QMessageBox.Information)
        mensaje.setText(text)
        mensaje.setWindowTitle(title)
        mensaje.exec_()

    def Agregar_a_la_Base(self):
        nombre = self.ui.tx_Nombre.text().strip()
        apellido = self.ui.tx_Apellido.text().strip()
        numero = self.ui.tx_Numero_inscripcion.text().strip()
        cedula = self.ui.tx_Cedula.text().strip()
        fecha = self.ui.tx_Fecha_nacimiento.text().strip()
        pais = self.ui.tx_Pais_origen.text().strip()
        equipo = self.ui.tx_Numero_equipo.text().strip()
        ranking = self.ui.tx_Ranquing_UCI.text().strip()

        if not all([nombre, apellido, numero, cedula, fecha, pais, equipo, ranking]):
            self._show_message("No están llenos todos los campos.", "Advertencia")
            return

        try:
            self.db.add_cyclist(nombre, apellido, numero, cedula, fecha, pais, equipo, ranking)
        except (ValueError, Exception) as exc:
            self._show_message(f"Error al registrar ciclista: {exc}", "Error")
            return

        self.ui.tx_Nombre.clear()
        self.ui.tx_Apellido.clear()
        self.ui.tx_Numero_inscripcion.clear()
        self.ui.tx_Cedula.clear()
        self.ui.tx_Fecha_nacimiento.clear()
        self.ui.tx_Pais_origen.clear()
        self.ui.tx_Numero_equipo.clear()
        self.ui.tx_Ranquing_UCI.clear()

        self._show_message("El ciclista se ha agregado.", "Registro exitoso")

    def Consultar_base(self):
        orden = self.ui.Escoger_orden.currentText()
        filas = self.db.list_cyclists(order_by=orden)

        self.ui.Tabla.setRowCount(len(filas))
        for cont, row in enumerate(filas):
            for col_idx, value in enumerate(row):
                self.ui.Tabla.setItem(cont, col_idx, QtWidgets.QTableWidgetItem(str(value)))

    def Borrar_ciclista(self):
        numero_borrar = self.ui.Num_ciclista_borrar.text().strip()
        if not numero_borrar:
            self._show_message("El campo está vacío.", "Advertencia")
            return

        try:
            deleted = self.db.delete_cyclist(numero_borrar)
        except ValueError:
            self._show_message("El número de inscripción debe ser entero.", "Error")
            return

        self.ui.Num_ciclista_borrar.clear()
        if deleted > 0:
            self._show_message("El ciclista se ha eliminado.", "Eliminación exitosa")
        else:
            self._show_message("No se encontró un ciclista con ese número.", "Aviso")

    def cambiar_nacionalidad(self):
        numero_cambio = self.ui.Num_ciclista_cambio.text().strip()
        nueva_nacionalidad = self.ui.Nueva_nacionalidad.text().strip()
        if not numero_cambio or not nueva_nacionalidad:
            self._show_message("No están todos los campos llenos.", "Advertencia")
            return

        try:
            updated = self.db.update_nationality(numero_cambio, nueva_nacionalidad)
        except ValueError:
            self._show_message("El número de inscripción debe ser entero.", "Error")
            return

        self.ui.Num_ciclista_cambio.clear()
        self.ui.Nueva_nacionalidad.clear()
        if updated > 0:
            self._show_message("La nacionalidad ha sido actualizada.", "Actualización exitosa")
        else:
            self._show_message("No se encontró un ciclista con ese número.", "Aviso")

    def Salir(self):
        self.db.close()
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    application = mywindow()
    application.show()
    sys.exit(app.exec())
