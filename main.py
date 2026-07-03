from PyQt5.QtCore import QSize
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from unicodedata import digit

from scripts.game_script import Game
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SuperDigit")
        self.setFixedSize(QSize(800, 600))
        uic.loadUi("mainwindow.ui", self)
        self.is_game = False
        self.check_btn.clicked.connect(self.make_guess)
        self.start_or_exit_game.clicked.connect(self.start_stop_game)
        self.plus_one_btn.clicked.connect(self.plus_one)
        self.minus_one_btn.clicked.connect(self.minus_one)

    def make_guess(self):
        if self.is_game == False:
            QMessageBox.critical(self, "Ошибка!", "Сперва начните игру!")
            return
        digit = int(self.digit.text())
        result = self.game.guess(digit)
        self.attempt_cd.display(self.game.attempts)
        self.result.setText(result)
        self.our_digit.setText(str(digit))
        if self.game.is_win == True:
            self.is_game = False
            self.game = 0
            self.start_or_exit_game.setText("Начать игру")
            self.start_or_exit_game.setStyleSheet("background-color: rgb(112, 222, 125);")
            self.is_chenge.setText("Да")
            self.name_frame.setStyleSheet("background-color: rgb(112, 222, 125);")

    def start_stop_game(self):
        if self.is_game == False:
            name = self.settings_name_btn.text()
            try:
                min_range = int(self.settings_min_range_btn.text())
                max_range = int(self.settings_max_range_btn.text())
            except:
                QMessageBox.critical(self, "Ошибка!", "Введите число!")
                return
            if max_range <= min_range:
                QMessageBox.critical(self, "Ошибка!", "Второе число дожно быть больше первого!")
                return
            if name != "" and min_range >= 0 and max_range >= 0:
                self.start_or_exit_game.setText("Отменить игру")
                self.is_chenge.setText("Нет")
                self.start_or_exit_game.setStyleSheet("background-color: rgb(255, 106, 108);")
                self.range_label.setText(f"Загадано число: от {min_range} до {max_range}")
                self.attempt_cd.display(0)
                self.name_frame.setStyleSheet("background-color: rgb(239, 233, 195);")

                self.game = Game(name, min_range, max_range)
                self.is_game = True
            else:
                QMessageBox.critical(self, "Ошибка!", "Введите имя и проложительные числа!")
                return
            return
        if self.is_game == True:
            self.game = 0
            self.is_game = False
            self.start_or_exit_game.setText("Начать игру")
            self.start_or_exit_game.setStyleSheet("background-color: rgb(112, 222, 125);")
            self.is_chenge.setText("Да")
            self.attempt_cd.display(0)
            return

    def plus_one(self):
        try:
            self.digit.setText(str(int(self.digit.text()) + 1))
        except:
            QMessageBox.critical(self, "Ошибка!", "Введите число!")
            return


    def minus_one(self):
        if int(self.digit.text()) == 0:
            return
        try:
            self.digit.setText(str(int(self.digit.text()) - 1))
        except:
            QMessageBox.critical(self, "Ошибка!", "Введите число!")
            return

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
