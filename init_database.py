#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных
"""

import sys
import os

# Добавляем путь к модулям
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from fin.db.init_db import init_db

def main():
    print("Инициализация базы данных...")
    try:
        init_db()
        print("База данных успешно инициализирована!")
        print("Файл базы данных создан в: src/fin/db/finance.db")
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")

if __name__ == "__main__":
    main() 