import sqlite3
import os

# Получаем путь к директории с базой данных
DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_name = os.path.join(DB_DIR, 'finance.db')

def init_db():
    with sqlite3.connect(DB_name) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS  categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL  UNIQUE
            )
            """ 
        )
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS  payments(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name    TEXT,
                       date DATE  NOT NULL,
                       amount INTEGER NOT NULL,
                       type TEXT NOT NULL,
                       category_id INTEGER ,
                       FOREIGN KEY (category_id) REFERENCES categories (id)
                       
                       )
                       """
        )
        conn.commit()
