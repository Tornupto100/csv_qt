import sys

import pandas
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt,pyqtSignal
import pandas as pd
from PyQt5.QtWidgets import QPushButton, QFileDialog, QLineEdit, QFormLayout, QLabel, QComboBox
from PyQt5.QtGui import QIcon, QFont

class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.count = None
        self.data = pd.DataFrame({'Load your csv': []})
        self.name = None
        self.initMe() # Erstelle die GUI


    def initMe(self):
        #self.data = pd.DataFrame({'Load your csv': []})
        #self.name = "Empty"
        #self.count = 0

        # Initilisiere Fenster
        self.setWindowTitle("CSV_Loader")
        #self.setWindowIcon(QIcon('Logo.png'))
        self.resize(800, 600)  # Größe des Fenster

        b_w = 675
        ## Widgets

        # Load Button
        self.load = QtWidgets.QPushButton("Load csv file first!", self)
        self.load.move(b_w,50)
        self.load.clicked.connect(self.openFileNameDialog)

        # Pandas Table + Sorting Functions
        self.table = QtWidgets.QTableView(self)
        self.table.setGeometry(50, 50, 600, 500)
        self.model = TableModel(self.data)  # Instanziere Daten ? Nur wie?
        self.table.setModel(self.model)
        self.table.horizontalHeader().sectionClicked.connect(self.ascentSort_header)
        self.table.horizontalHeader().sectionDoubleClicked.connect(self.descentSort_header)
        #self.table.clicked.connect(self.ascentSort_old())
        #self.table.doubleClicked.connect(self.descentSort_old())

        # 2. LineEdit Seperator
        self.line = QLineEdit(self)
        self.line.setMaxLength(1)
        self.line.setPlaceholderText("Enter sep[, or .]")
        self.line.textChanged.connect(self.seperator_added)
        self.line.move(b_w, 100)

        # 3. Combobox Delimiter
        self.cb = QComboBox(self)
        self.cb.move(b_w, 150)
        self.cb.addItems([".", ","])
        self.cb.currentIndexChanged.connect(self.selectionchange)

        # 4. Reset
        reset = QPushButton("Reset", self)
        reset.move(b_w, 200)
        #button3.setGeometry(400,400,100,50)
        reset.clicked.connect(self.reset_file)  # Verbindet ein Event hier

        # 5.Export Button
        export = QPushButton("Export to xls", self)
        export.move(b_w, 250)
        #export.setGeometry(400,400,100,50)
        export.clicked.connect(self.save_file)  # Verbindet ein Event hier

    def openFileNameDialog(self):
            #options = QFileDialog.Options()
            #options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                      "CSV Files (*.csv)")

            #fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
             #                                         "All Files (*);;CSV Files (*.csv)")
            if fileName:
                #print(fileName)
                #print("Data is selected")
                self.name = fileName
                self.update_data(pd.read_csv(fileName)) # Only Valid for header files

    def reset_file(self):
            if self.name:
                self.update_data(pd.read_csv(self.name))

    def seperator_added(self, s): # Decimal Operator --> Integrate default into selection
        #print(s)
        #print(self.line.text())
        #print(self.cb.currentText())
        #print("next")

        if s:
            #print(self.name)
            if self.cb.currentText():
                data = pd.read_csv(self.name, decimal=s, delimiter=self.cb.currentText(), engine='python')
            else:
                data = pd.read_csv(self.name, decimal=s, engine='python')
            self.update_data(data)

    def selectionchange(self, i): # Delimeter Selector
        print(i)
        print(self.line.text())
        print(self.cb.currentText())
        if self.line.text():
            data = pd.read_csv(self.name, decimal=self.line.text(), delimiter=self.cb.currentText(), engine='python')
        else:
            data = pd.read_csv(self.name, delimiter=self.cb.currentText(), engine='python')
        self.update_data(data)

    def save_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "xlsx Files (*.xlsx)", options=options)
        if fileName:
            print(fileName)
            fileName = fileName + ".xlsx"
            self.data.to_excel(fileName)
            print("Export zu Excel")

    def update_data(self,data):
        assert isinstance(data, pd.DataFrame)
        self.model._data = data
        self.data = data
        self.model.layoutChanged.emit()

    def ascentSort_header(self, i):
        #print("index clicked is" + str(i))
        header = self.data.columns[i][:]
        data = self.data.sort_values(by=header, ascending=True)
        self.update_data(data)

    def descentSort_header(self, i):
        #print("index clicked is" + str(i))
        header = self.data.columns[i][:]
        data = self.data.sort_values(by=header, ascending=False)
        self.update_data(data)

    def ascentSort_old(self, i):
        # Selection via Fields
        # http://www.python-forum.org/viewtopic.php?f=11&t=16817
        sf = "You clicked on {0}x{1}".format(item.column(), item.row())
        col= type(item.column())
        header=self.data.columns[item.column()][:]
        print(col)
        print("oneClick")
        data = self.data.sort_values(by=header,ascending=True)
        self.model._data = data
        self.data = data
        self.model.layoutChanged.emit()

    def descentSort_old(self, item):
        # Selection via Fields, not used
        print("DoubleClick")
        # http://www.python-forum.org/viewtopic.php?f=11&t=16817
        sf = "You clicked on {0}x{1}".format(item.column(), item.row())
        col=type(item.column())
        header=self.data.columns[item.column()][:]
        print(col)
        print(header)
        data = self.data.sort_values(by=header,ascending=False)
        self.model._data = data
        self.data = data
        self.model.layoutChanged.emit()


app=QtWidgets.QApplication(sys.argv)
window=MainWindow()
window.show()
app.exec_()