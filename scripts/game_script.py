import random


class Game:
    def __init__(self, name: str, min_range: int, max_range: int):
        self.name = name
        self.min_range = min_range
        self.max_range = max_range
        self.secret = random.randint(min_range, max_range)
        self.attempts = 0
        self.last_guess = 0
        self.record = 0
        self.is_win = False

    def guess(self, digit):
        if digit < self.secret:
            self.attempts += 1
            self.last_guess = digit
            return "Больше"
        if digit > self.secret:
            self.attempts += 1
            self.last_guess = digit
            return "Меньше"
        if digit == self.secret:
            self.attempts +=1
            self.is_win = True
            self.record = (self.max_range - self.min_range) * (1 / self.attempts)
            return "Вы угадали"