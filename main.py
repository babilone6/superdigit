from PyQt5.QtCore import QSize
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon

from scripts.game_script import Game
from scripts.db_script import DataBase

import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(800, 600))
        uic.loadUi("mainwindow.ui", self)
        self.setWindowIcon(QIcon("img/ico.png"))
        self.setWindowTitle("Super Digit")
        self.is_game = False

        self.check_btn.clicked.connect(self.make_guess)
        self.start_or_exit_game.clicked.connect(self.start_stop_game)
        self.plus_one_btn.clicked.connect(self.plus_one)
        self.minus_one_btn.clicked.connect(self.minus_one)
        self.preset_btn1.clicked.connect(self.preset)
        self.preset_btn2.clicked.connect(self.preset)
        self.preset_btn3.clicked.connect(self.preset)
        self.preset_btn4.clicked.connect(self.preset)
        self.preset_btn5.clicked.connect(self.preset)
        self.preset_btn6.clicked.connect(self.preset)
        self.preset_btn7.clicked.connect(self.preset)
        self.preset_btn8.clicked.connect(self.preset)
        self.preset_btn9.clicked.connect(self.preset)
        self.preset_btn10.clicked.connect(self.preset)
        self.anonim_btn.clicked.connect(self.anonim_name)
        self.use_last_name_btn.clicked.connect(self.last_name)

        self.db = DataBase()
        record = self.db.get_record()
        if record != None:
            record = list(map(str, record))
            self.name.setText(record[0])
            self.min_range.setText(record[1])
            self.max_range.setText(record[2])
            self.secret.setText(record[3])
            self.attempts.setText(record[4])
            self.last_guess.setText(record[5])

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
            self.result.setText("Неизвестно")
            return

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
            self.db.add_record(self.game.name, self.game.record, self.game.min_range, self.game.max_range,
                               self.game.secret, self.game.attempts, self.game.last_guess)
            record = self.db.get_record()
            if record is None:
                record = list(map(str, record))
                self.name.setText(record[0])
                self.min_range.setText(record[1])
                self.max_range.setText(record[2])
                self.secret.setText(record[3])
                self.attempts.setText(record[4])
                self.last_guess.setText(record[5])
            self.game = 0
            self.start_or_exit_game.setText("Начать игру")
            self.start_or_exit_game.setStyleSheet("background-color: rgb(112, 222, 125);")
            self.is_chenge.setText("Да")
            self.name_frame.setStyleSheet("background-color: rgb(112, 222, 125);")

    def plus_one(self):
        try:
            self.digit.setValue(int(self.digit.value()) + 1)
        except:
            QMessageBox.critical(self, "Ошибка!", "Введите число!")
            return

    def minus_one(self):
        if int(self.digit.value()) == 0:
            return
        try:
            self.digit.setValue(int(self.digit.value()) - 1)
        except:
            QMessageBox.critical(self, "Ошибка!", "Введите число!")
            return

    def preset(self):
        btn = self.sender()
        min_range, max_range = btn.text().split("-")
        self.settings_min_range_btn.setText(min_range)
        self.settings_max_range_btn.setText(max_range)

    def anonim_name(self):
        self.settings_name_btn.setText("Аноним")

    def last_name(self):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT name FROM records ORDER BY id DESC LIMIT 1")
        name = cursor.fetchone()
        if name is None:
            QMessageBox.critical(self, "Ошибка!", "Вы ещё не сыграли ни одной игры!")
        else:
            self.settings_name_btn.setText(name[0])

    def closeEvent(self, event):
        self.db.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
