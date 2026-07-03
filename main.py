from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QMainWindow
import sys



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SuperDigit")
        self.setFixedSize(QSize(400, 600))

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()