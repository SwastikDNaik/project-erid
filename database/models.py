from database.db import cursor, conn

def create_tables():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        type TEXT,
        amount REAL,
        category TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budget (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        monthly_budget REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        amount REAL,
        frequency TEXT,
        due_date TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS savings (
        id INTEGER PRIMARY KEY,
        amount REAL
    )
    """)
    
    cursor.execute("""
    INSERT OR IGNORE INTO savings(id, amount)
    VALUES (1, 0)
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS paid_bills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bill_id INTEGER,
        paid_date TEXT
    )
    """)

    conn.commit()