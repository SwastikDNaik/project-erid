import sqlite3

conn = sqlite3.connect(
    "data/Erid_data.db",
    check_same_thread=False
)

cursor = conn.cursor()