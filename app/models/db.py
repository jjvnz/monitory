import sqlite3

def init_db(app):
    with sqlite3.connect('metrics.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            cpu_percent REAL,
            memory_percent REAL,
            disk_percent REAL
        )
        ''')
        conn.commit()

def get_db():
    return sqlite3.connect('metrics.db')
