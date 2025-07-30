#!/usr/bin/env python3
"""
Скрипт для добавления тестовых данных
"""

import sys
import os
from datetime import datetime, timedelta

# Добавляем путь к модулям
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from fin.db.database import add_category
from fin.db.DB_payment import add_payment

def add_test_data():
    print("Добавление тестовых данных...")
    
    # Добавляем категории
    categories = [
        "Продукты",
        "Транспорт", 
        "Развлечения",
        "Зарплата",
        "Фриланс"
    ]
    
    category_ids = {}
    for category in categories:
        try:
            add_category(category)
            print(f"✓ Добавлена категория: {category}")
        except:
            print(f"⚠ Категория уже существует: {category}")
    
    # Получаем ID категорий
    from fin.db.database import get_all_category
    categories_data = get_all_category()
    for cat_id, cat_name in categories_data:
        category_ids[cat_name] = cat_id
    
    # Добавляем тестовые платежи за последние 30 дней
    today = datetime.now()
    
    # Доходы
    payments = [
        # Зарплата
        ("Зарплата за месяц", today - timedelta(days=25), 50000, "income", "Зарплата"),
        ("Зарплата за месяц", today - timedelta(days=5), 50000, "income", "Зарплата"),
        
        # Фриланс
        ("Проект веб-сайта", today - timedelta(days=15), 15000, "income", "Фриланс"),
        ("Консультация", today - timedelta(days=8), 5000, "income", "Фриланс"),
        
        # Расходы - Продукты
        ("Продукты в магазине", today - timedelta(days=1), 2500, "expense", "Продукты"),
        ("Продукты в магазине", today - timedelta(days=3), 1800, "expense", "Продукты"),
        ("Продукты в магазине", today - timedelta(days=7), 3200, "expense", "Продукты"),
        ("Продукты в магазине", today - timedelta(days=12), 2100, "expense", "Продукты"),
        ("Продукты в магазине", today - timedelta(days=18), 2800, "expense", "Продукты"),
        
        # Расходы - Транспорт
        ("Такси", today - timedelta(days=2), 500, "expense", "Транспорт"),
        ("Метро", today - timedelta(days=4), 200, "expense", "Транспорт"),
        ("Такси", today - timedelta(days=6), 800, "expense", "Транспорт"),
        ("Метро", today - timedelta(days=10), 200, "expense", "Транспорт"),
        ("Такси", today - timedelta(days=14), 600, "expense", "Транспорт"),
        
        # Расходы - Развлечения
        ("Кино", today - timedelta(days=5), 1200, "expense", "Развлечения"),
        ("Ресторан", today - timedelta(days=9), 3500, "expense", "Развлечения"),
        ("Кино", today - timedelta(days=16), 1200, "expense", "Развлечения"),
        ("Ресторан", today - timedelta(days=20), 2800, "expense", "Развлечения"),
    ]
    
    for name, date, amount, payment_type, category_name in payments:
        if category_name in category_ids:
            add_payment(name, date.strftime("%Y-%m-%d"), amount, payment_type, category_ids[category_name])
            print(f"✓ Добавлен платеж: {name} - {amount} ₽ ({payment_type})")
    
    print("\n✅ Тестовые данные успешно добавлены!")
    print("Теперь вы можете протестировать все функции приложения.")

if __name__ == "__main__":
    add_test_data() 