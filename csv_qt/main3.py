import sys
from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QPushButton, QFileDialog, QLineEdit, QVBoxLayout, QLabel, QComboBox, \
    QTableWidgetItem


class MainWindow(QtWidgets.QMainWindow):
    updateSignal = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.table_widget = QTableWidget()
        self.button = QPushButton('Populate')
        self.button.clicked.connect(self.populate)
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.updateSignal.connect(self.update_table)
        self.populate()

    def populate(self):
        nrows, ncols = 5, 2
        self.table_widget.setSortingEnabled(False)
        self.table_widget.setRowCount(nrows)
        self.table_widget.setColumnCount(ncols)
        for i in range(nrows):
            for j in range(ncols):
                item = QTableWidgetItem('%s%s' % (i, j))
                self.table_widget.setItem(i, j, item)
        self.updateSignal.emit()
        self.table_widget.setSortingEnabled(True)

    def update_table(self):
        self.table_widget.sortItems(0,QtCore.Qt.DescendingOrder)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    wnd = MainWindow()
    wnd.resize(640, 480)
    wnd.show()
    sys.exit(app.exec_())
