import sqlite3

def init_db():
    conn = sqlite3.connect('db/project.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            coins INTEGER NOT NULL,
            password TEXT NOT NULL,
            inset INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()