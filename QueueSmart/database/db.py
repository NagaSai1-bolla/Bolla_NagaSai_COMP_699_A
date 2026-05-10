import sqlite3

DB_PATH = "database/queuesmart.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    with open("database/schema.sql", "r") as f:
        conn.executescript(f.read())

    conn.commit()
    conn.close()