import sys
# 1. Importiere Bib
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtCore import *
#from PyQt5.QtGui import *


if __name__ == '__main__':
# 2.Erstelle eine Instanz von Q Application
    app = QApplication(sys.argv) # sys argv beinhaltet eine list von argumentrs zu parsen

#3 Erstelle eine GUI

    fenster = QWidget()
    fenster.setWindowTitle("Meine erste App")
    fenster.setGeometry(100,100,280,80) # Größe des Fensters
    fenster.move(60,15) # Verschiebe auf Bildschirm
    #helloMsg = QLabel('<h1> Hallo Welt <h1>!',parent=fenster)
    helloMsg = QLabel("Das ist ein Text",parent=fenster)
    helloMsg.setPixmap(QPixmap('Logo.png'))
    helloMsg.move(60,15)

    # Jede funktionale GUI braucht ein Widget!
    # Parent (Widget in widget) sonst Hauptansicht, damit alle anderen Widgets auchgelöscht werdne

    # 4. Anzeige
    fenster.show()

    # 5 Run in a loop
    sys.exit(app.exec_())