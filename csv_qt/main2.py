import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
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
        self.initMe() # Erstelle die GUI


    def initMe(self):
        self.data = pd.DataFrame({'Load your csv': []})
        self.name = "Empty"
        self.count = 0

        # Initilisiere Fenster
        self.setWindowTitle("CSV_Loader")
        self.setWindowIcon(QIcon('Logo.png'))
        self.resize(600, 600)  # Größe des Fenster

        ## Widgets

        # Load Button
        self.button1 = QtWidgets.QPushButton("Upload csv file first", self)
        self.button1.move(450,50)
        self.button1.clicked.connect(self.openFileNameDialog)

        # Pandas Table
        self.table = QtWidgets.QTableView(self)
        self.table.setGeometry(50, 50, 350, 500)
        self.model = TableModel(self.data)  # Instanziere Daten ? Nur wie?
        self.table.setModel(self.model)
        self.table.clicked.connect(self.ascentSort)
        self.table.doubleClicked.connect(self.descentSort)
        # 3 times clicked /

        # 2. LineEdit Seperator
        self.line = QLineEdit(self)
        self.line.setMaxLength(1)
        self.line.setPlaceholderText("Enter sep[, or .]")
        self.line.textChanged.connect(self.seperator_added)
        self.line.move(450, 100)

        # 3. Combobox Delimiter
        self.cb = QComboBox(self)
        self.cb.move(450, 150)
        self.cb.addItems([".", ","])
        self.cb.currentIndexChanged.connect(self.selectionchange)

        # 4.Export Button
        button3 = QPushButton("Export to xls", self)
        button3.move(450, 200)
        #button3.setGeometry(400,400,100,50)
        button3.clicked.connect(self.save_file)  # Verbindet ein Event hier

    def openFileNameDialog(self):
            #options = QFileDialog.Options()
            #options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                      "All Files (*);;CSV Files (*.csv)")
            if fileName:
                #print(fileName)
                #print("Data is selected")
                self.name = fileName
                data=pd.read_csv(fileName)
                self.model._data = data
                self.data = data
                self.model.layoutChanged.emit()

    def seperator_added(self, s): # Decimal Operator --> Integrate default into selection
        if s:
            #print(self.name)
            data = pd.read_csv(self.name, decimal=s, engine='python')
            self.model._data = data
            self.data = data
            self.model.layoutChanged.emit()

    def selectionchange(self, i): # Delimeter Selector
        data = pd.read_csv(self.name, delimiter=self.cb.currentText(), engine='python')
        self.model._data = data
        self.data = data
        self.model.layoutChanged.emit()

    def save_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "xlsx Files (*.xlsx)", options=options)
        if fileName:
            print(fileName)
            fileName =fileName + ".xlsx"
            self.data.to_excel(fileName)
            print("Export zu Excel")



        #print("Export zu Excel")
        #if self.name != None:
         #   self.data.to_excel("output.xlsx")

    def counter(self):
        self.data.sort_values(axis=1)

    def ascentSort(self, item):
        # http://www.python-forum.org/viewtopic.php?f=11&t=16817
        sf = "You clicked on {0}x{1}".format(item.column(), item.row())
        col=type(item.column())
        header=self.data.columns[item.column()][:]
        print(col)
        print("oneClick")
        data = self.data.sort_values(by=header,ascending=True)
        self.model._data = data
        self.data = data
        self.model.layoutChanged.emit()

    def descentSort(self, item):
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

"Just a comment"
app=QtWidgets.QApplication(sys.argv)
window=MainWindow()
window.show()
app.exec_()