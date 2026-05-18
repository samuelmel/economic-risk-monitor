import sqlite3
from pathlib import Path

from config import DATABASE_PATH


class Database:
    def __init__(self):
        DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
        self.database_path = DATABASE_PATH

    def connect(self):
        return sqlite3.connect(self.database_path)

    def execute_script(self, sql_file: Path) -> None:
        with self.connect() as connection:
            with sql_file.open("r", encoding="utf-8") as file:
                connection.executescript(file.read())