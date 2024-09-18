import sqlite3

def get_historical_data():
    conn = sqlite3.connect('metrics.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT timestamp, cpu_percent, memory_percent, disk_percent FROM metrics
    ORDER BY timestamp DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows
