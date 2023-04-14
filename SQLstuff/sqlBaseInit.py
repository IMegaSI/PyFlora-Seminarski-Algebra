import sqlite3

def DBusers():
    DB = "baza.db"
    conn = sqlite3.connect(DB)
    return conn
