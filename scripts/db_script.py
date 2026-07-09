import sqlite3
import os


class DataBase:
    def __init__(self):
        if not os.path.exists("./data.db"):
            self.conn = sqlite3.connect("./data.db")
            self.cursor = self.conn.cursor()
            self.cursor.execute("""
                CREATE TABLE records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    record INTEGER,
                    min_range INTEGER,
                    max_range INTEGER,
                    secret INTEGER,
                    attempts INTEGER,
                    last_guess INTEGER
                );
            """)
            self.conn.commit()

        else:
            self.conn = sqlite3.connect("./data.db")
            self.cursor = self.conn.cursor()



    def add_record(self, name: str, record: int, min_range: int, max_range: int, secret: int, attempts: int, last_guess: int):
        self.cursor.execute(f"INSERT INTO records (name, record, min_range, max_range, secret, attempts, last_guess) VALUES ('{name}', {record}, {min_range}, {max_range}, {secret}, {attempts}, {last_guess})")
        self.conn.commit()

    def get_record(self):
        self.cursor.execute("SELECT name, min_range, max_range, secret, attempts, last_guess FROM records ORDER BY record DESC LIMIT 1")
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()


