import sqlite3
from config.settings import DATABASE_PATH

def connect_db():
    return sqlite3.connect(DATABASE_PATH)

def create_tables():
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    print("Создание таблицы users...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        role TEXT,
        login TEXT,
        password TEXT,
        birthdate TEXT,
        avatar TEXT
    )""")

    print("Создание таблицы equipment...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS equipment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        weight INTEGER,
        size INTEGER,
        temperature INTEGER,
        condition BOOLEAN
    )""")

    print("Создание таблицы checks...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS checks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        equipment_id INTEGER,
        info TEXT,
        date TEXT,
        count INTEGER,
        fallability REAL,
        display_date BOOLEAN DEFAULT 1,
        display_count BOOLEAN DEFAULT 1,
        display_fallability BOOLEAN DEFAULT 1,
        FOREIGN KEY (equipment_id) REFERENCES equipment(id)
    )""")

    print("Создание таблицы reports...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        info TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,  -- Новое поле
        FOREIGN KEY (user_id) REFERENCES users(id)
    )""")

    print("Создание таблицы tests...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        weight INTEGER,
        size INTEGER,
        temperature INTEGER
    )""")

    conn.commit()
    conn.close()

    print("Все таблицы созданы.")
