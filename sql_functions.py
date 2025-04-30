import sqlite3


def initiate_sql():
    conn = sqlite3.connect('finance_data.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS finance_entries (
    id INTEGER PRIMARY KEY,
    date TEXT,
    amount REAL,
    type TEXT,
    description TEXT
    );''')
    conn.commit()
    conn.close()


def fetch_all_data():
    conn = sqlite3.connect('finance_data.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM finance_entries;
    ''')
    data = cursor.fetchall()
    conn.close()
    return data


def insert_row(date, amount, type, description):
    conn = sqlite3.connect('finance_data.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO finance_entries (date, amount, type, description) VALUES (?, ?, ?, ?)'''
                   , (date, amount, type, description))
    conn.commit()
    conn.close()


def delete_row(row_id):
    conn = sqlite3.connect('finance_data.db')
    cursor = conn.cursor()
    cursor.execute('''
    DELETE FROM finance_entries WHERE id = ?
    ''', (row_id,))
    conn.commit()
    conn.close()
