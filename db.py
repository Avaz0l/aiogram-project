import sqlite3

# Путь к базе данных
DB_PATH = 'bot.db'


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def init_db(self):

        # Создаем таблицу правильно
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                state TEXT
            )
        ''')
        self.connection.commit()

    def update_state(self, user_id, state):

        self.cursor.execute(
            "INSERT OR IGNORE INTO Users (id, state) VALUES (?, ?)", (user_id, ''))

        self.cursor.execute(
            "UPDATE Users SET state = ? WHERE id = ?", (state, user_id))
        self.connection.commit()

    def get_state(self, user_id):

        self.cursor.execute("SELECT state FROM Users WHERE id = ?", (user_id,))
        result = self.cursor.fetchone()

        return result[0] if result else None
