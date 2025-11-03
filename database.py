import sqlite3
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS payouts (
            name TEXT PRIMARY KEY,
            caller TEXT,
            total REAL,
            repairs REAL,
            guild_percent REAL,
            guild_cut REAL,
            net REAL,
            per_member REAL,
            validated INTEGER DEFAULT 0
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS payout_users (
            payout_name TEXT,
            user_id INTEGER
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS user_balances (
            user_id INTEGER PRIMARY KEY,
            balance REAL DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()