from PyQt5.QtCore import QSize
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SuperDigit")
        self.setFixedSize(QSize(800, 600))
        uic.loadUi("mainwindow.ui", self)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()