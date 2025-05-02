import sqlite3


def initiate_sql():
    conn = None
    try:
        conn = sqlite3.connect('finance_data.db')
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS finance_entries (
        id INTEGER PRIMARY KEY,
        date TEXT,
        amount REAL,
        category TEXT,
        description TEXT
        );''')
        conn.commit()
    except sqlite3.Error as error:
        if conn:
            conn.rollback()
            print(f"SQL Couldn't init: {error}")
    finally:
        if conn:
            conn.close()


def fetch_all_data():
    conn = None
    data = None
    try:
        conn = sqlite3.connect('finance_data.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM finance_entries ORDER BY date(date) ASC;
        ''')
        data = cursor.fetchall()
    except sqlite3.Error as error:
        if conn:
            conn.rollback()
            print(f"Select failed {error}")
    finally:
        if conn:
            conn.close()
        return data


def insert_row(date, amount, category, description):
    conn = None
    try:
        conn = sqlite3.connect('finance_data.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO finance_entries (date, amount, category, description) VALUES (?, ?, ?, ?)'''
                       , (date, amount, category, description))
        conn.commit()
    except sqlite3.Error as error:
        if conn:
            conn.rollback()
            print(f"SQL error, entry: {error}")
    finally:
        if conn:
            conn.close()


def delete_row(row_id):
    conn = None
    try:
        conn = sqlite3.connect('finance_data.db')
        cursor = conn.cursor()
        cursor.execute('''
        DELETE FROM finance_entries WHERE id = ?
        ''', (row_id,))
        conn.commit()
    except sqlite3.Error as error:
        if conn:
            conn.rollback()
            print(f"SQL error on: {row_id} : {error}")
    finally:
        if conn:
            conn.close()

