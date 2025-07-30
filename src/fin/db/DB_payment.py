import sqlite3
import os
from typing import Optional, List, Tuple, Dict, Any
from datetime import datetime

# Получаем путь к директории с базой данных
DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_name = os.path.join(DB_DIR, 'finance.db')

print(str(datetime.today())[:10])
def add_payment(name, date, amount, type,category_id):
    with sqlite3.connect(DB_name) as conn:
        cursor = conn.cursor()
        try:
            if name == '':
                name = 'Без названия'
            if date == '':
                date = str(datetime.today())[:10]
            cursor.execute(" INSERT INTO payments (name , date, amount, type,  category_id) VALUES (?,?,?,?,?) ", (name, date, amount, type, category_id))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f'Errof - {e}')
            return None

# Убираем тестовый код
# add_payment('tualet2' , '', 9000, 'pipi',2)

def del_payment(payment_id):
    with sqlite3.connect(DB_name) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM payments WHERE id = ?" ,(payment_id,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f' Error in del pay{e}')
            return None
    

def get_payment_by_category(category_id):
    with sqlite3.connect(DB_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, date, amount, type FROM payments WHERE category_id = ? ORDER BY date DESC", (category_id,))
        return cursor.fetchall()

def get_total_statistics():
    """Получить общую статистику по доходам и расходам"""
    with sqlite3.connect(DB_name) as conn:
        cursor = conn.cursor()
        
        # Общий доход
        cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM payments WHERE type = 'income'")
        total_income = cursor.fetchone()[0]
        
        # Общий расход
        cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM payments WHERE type = 'expense'")
        total_expense = cursor.fetchone()[0]
        
        # Баланс
        balance = total_income - total_expense
        
        return {
            'income': total_income,
            'expense': total_expense,
            'balance': balance
        }

def get_statistics_by_date_range(date_from, date_to):
    """Получить статистику по диапазону дат"""
    with sqlite3.connect(DB_name) as conn:
        cursor = conn.cursor()
        
        # Доходы за период
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0) 
            FROM payments 
            WHERE type = 'income' AND date BETWEEN ? AND ?
        """, (date_from, date_to))
        total_income = cursor.fetchone()[0]
        
        # Расходы за период
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0) 
            FROM payments 
            WHERE type = 'expense' AND date BETWEEN ? AND ?
        """, (date_from, date_to))
        total_expense = cursor.fetchone()[0]
        
        # Баланс за период
        balance = total_income - total_expense
        
        # Данные для графика (по дням)
        cursor.execute("""
            SELECT date, 
                   SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as income,
                   SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as expense
            FROM payments 
            WHERE date BETWEEN ? AND ?
            GROUP BY date 
            ORDER BY date
        """, (date_from, date_to))
        
        chart_data = cursor.fetchall()
        
        return {
            'income': total_income,
            'expense': total_expense,
            'balance': balance,
            'chart_data': chart_data
        }

def get_category_statistics(category_id):
    """Получить статистику для конкретной категории"""
    with sqlite3.connect(DB_name) as conn:
        cursor = conn.cursor()
        
        # Доходы в категории
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0) 
            FROM payments 
            WHERE category_id = ? AND type = 'income'
        """, (category_id,))
        total_income = cursor.fetchone()[0]
        
        # Расходы в категории
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0) 
            FROM payments 
            WHERE category_id = ? AND type = 'expense'
        """, (category_id,))
        total_expense = cursor.fetchone()[0]
        
        return {
            'income': total_income,
            'expense': total_expense
        }
    
# Убираем тестовый код
# print(get_payment_by_category(2))

def update_payment():
    pass 

# def get_payment_by_type(type_payment):
#     with sqlite3.connect(DB_name) as conn:
#         cursor = conn.cursor()
#         cursor.execute(""" SELECT id,  """)

##TODO переписать 
##КАСКАДНОЕ УДАЛЕНИЕ НЕ РАБОТАЕТ ПЕРЕДЕЛАТЬ Б



# def get_payments_smart_filter(
#     name_contains: Optional[str] = None,
#     date_exact: Optional[str] = None,
#     date_from: Optional[str] = None,
#     date_to: Optional[str] = None,
#     payment_type: Optional[str] = None,
#     amount_exact: Optional[float] = None,
#     amount_from: Optional[float] = None,
#     amount_to: Optional[float] = None,
#     category_id: Optional[int] = None,
#     category_name: Optional[str] = None,
#     limit: Optional[int] = None,
#     order_by: str = 'date',
#     order_desc: bool = True
# ) -> List[Tuple]:
#     """
#     Умная фильтрация платежей с множеством параметров
    
#     Args:
#         name_contains: Подстрока для поиска в названии
#         date_exact: Точная дата (формат: 'YYYY-MM-DD')
#         date_from: Начальная дата (включительно)
#         date_to: Конечная дата (включительно)
#         payment_type: Тип платежа ('income' или 'expense')
#         amount_exact: Точная сумма
#         amount_from: Минимальная сумма (включительно)
#         amount_to: Максимальная сумма (включительно)
#         category_id: ID категории
#         category_name: Название категории (для поиска по имени)
#         limit: Ограничение количества результатов
#         order_by: Поле для сортировки ('date', 'amount', 'name')
#         order_desc: Сортировка по убыванию (True) или возрастанию (False)
    
#     Returns:
#         Список кортежей с данными платежей
#     """
    
#     with sqlite3.connect(DB_name) as conn:
#         cursor = conn.cursor()
        
#         # Базовый запрос с JOIN для получения названия категории
#         query = """
#             SELECT p.id, p.name, p.date, p.amount, p.type, p.category_id, c.name as category_name
#             FROM payments p
#             LEFT JOIN categories c ON p.category_id = c.id
#             WHERE 1=1
#         """
        
#         params = []
        
#         # Фильтр по названию (частичное совпадение)
#         if name_contains:
#             query += " AND p.name LIKE ?"
#             params.append(f"%{name_contains}%")
        
#         # Точная дата
#         if date_exact:
#             query += " AND p.date = ?"
#             params.append(date_exact)
        
#         # Диапазон дат
#         if date_from:
#             query += " AND p.date >= ?"
#             params.append(date_from)
            
#         if date_to:
#             query += " AND p.date <= ?"
#             params.append(date_to)
        
#         # Тип платежа
#         if payment_type:
#             query += " AND p.type = ?"
#             params.append(payment_type)
        
#         # Точная сумма
#         if amount_exact is not None:
#             query += " AND p.amount = ?"
#             params.append(amount_exact)
        
#         # Диапазон сумм
#         if amount_from is not None:
#             query += " AND p.amount >= ?"
#             params.append(amount_from)
            
#         if amount_to is not None:
#             query += " AND p.amount <= ?"
#             params.append(amount_to)
        
#         # ID категории
#         if category_id is not None:
#             query += " AND p.category_id = ?"
#             params.append(category_id)
        
#         # Название категории
#         if category_name:
#             query += " AND c.name LIKE ?"
#             params.append(f"%{category_name}%")
        
#         # Сортировка
#         valid_order_fields = ['date', 'amount', 'name', 'p.date', 'p.amount', 'p.name']
#         if order_by in valid_order_fields or order_by.startswith('p.'):
#             order_direction = "DESC" if order_desc else "ASC"
#             query += f" ORDER BY {order_by} {order_direction}"
#         else:
#             order_direction = "DESC" if order_desc else "ASC"
#             query += f" ORDER BY p.date {order_direction}"
        
#         # Лимит
#         if limit:
#             query += " LIMIT ?"
#             params.append(limit)
        
#         try:
#             cursor.execute(query, params)
#             return cursor.fetchall()
#         except sqlite3.Error as e:
#             print(f"Ошибка при фильтрации платежей: {e}")
#             return []

# def get_payments_by_period_summary(
#     date_from: Optional[str] = None,
#     date_to: Optional[str] = None,
#     group_by: str = 'month'
# ) -> List[Tuple]:
#     """
#     Получить сводку по периодам
    
#     Args:
#         date_from: Начальная дата
#         date_to: Конечная дата
#         group_by: Группировка ('day', 'month', 'year')
    
#     Returns:
#         Сводка по периодам с суммами доходов и расходов
#     """
    
#     with sqlite3.connect(DB_name) as conn:
#         cursor = conn.cursor()
        
#         # Определяем формат даты для группировки
#         if group_by == 'day':
#             date_format = "%Y-%m-%d"
#             date_group = "p.date"
#         elif group_by == 'month':
#             date_format = "%Y-%m"
#             date_group = "substr(p.date, 1, 7)"
#         elif group_by == 'year':
#             date_format = "%Y"
#             date_group = "substr(p.date, 1, 4)"
#         else:
#             date_group = "substr(p.date, 1, 7)"  # default to month
        
#         query = f"""
#             SELECT 
#                 {date_group} as period,
#                 SUM(CASE WHEN p.type = 'income' THEN p.amount ELSE 0 END) as total_income,
#                 SUM(CASE WHEN p.type = 'expense' THEN p.amount ELSE 0 END) as total_expense,
#                 SUM(CASE WHEN p.type = 'income' THEN p.amount ELSE -p.amount END) as net_amount
#             FROM payments p
#             WHERE 1=1
#         """
        
#         params = []
        
#         if date_from:
#             query += " AND p.date >= ?"
#             params.append(date_from)
            
#         if date_to:
#             query += " AND p.date <= ?"
#             params.append(date_to)
        
#         query += f" GROUP BY {date_group} ORDER BY period DESC"
        
#         try:
#             cursor.execute(query, params)
#             return cursor.fetchall()
#         except sqlite3.Error as e:
#             print(f"Ошибка при получении сводки: {e}")
#             return []

# def search_payments_flexible(search_term: str) -> List[Tuple]:
#     """
#     Гибкий поиск по всем полям (название, категория)
    
#     Args:
#         search_term: Поисковый запрос
    
#     Returns:
#         Список найденных платежей
#     """
    
#     with sqlite3.connect(DB_name) as conn:
#         cursor = conn.cursor()
        
#         query = """
#             SELECT p.id, p.name, p.date, p.amount, p.type, p.category_id, c.name as category_name
#             FROM payments p
#             LEFT JOIN categories c ON p.category_id = c.id
#             WHERE p.name LIKE ? OR c.name LIKE ?
#             ORDER BY p.date DESC
#         """
        
#         search_pattern = f"%{search_term}%"
        
#         try:
#             cursor.execute(query, (search_pattern, search_pattern))
#             return cursor.fetchall()
#         except sqlite3.Error as e:
#             print(f"Ошибка при поиске: {e}")
#             return []

# # Примеры использования:
# if __name__ == "__main__":
#     # 1. Поиск по части названия
#     results = get_payments_smart_filter(name_contains="продукты")
    
#     # 2. Платежи за конкретный период
#     results = get_payments_smart_filter(
#         date_from="2024-01-01",
#         date_to="2024-01-31"
#     )
    
#     # 3. Расходы больше определенной суммы
#     results = get_payments_smart_filter(
#         payment_type="expense",
#         amount_from=1000.0
#     )
    
#     # 4. Комбинированный поиск
#     results = get_payments_smart_filter(
#         name_contains="магазин",
#         date_from="2024-01-01",
#         amount_to=5000.0,
#         order_by="amount",
#         order_desc=True,
#         limit=10
#     )
    
#     # 5. Поиск по категории
#     results = get_payments_smart_filter(
#         category_name="еда",
#         date_from="2024-01-01"
#     )
    
#     # 6. Гибкий поиск
#     results = search_payments_flexible("ресторан")
    
#     # 7. Сводка по месяцам
#     summary = get_payments_by_period_summary(
#         date_from="2024-01-01",
#         date_to="2024-12-31",
#         group_by="month"
#     )
    
#     print("Результаты поиска:")
#     for payment in results:
#         print(payment)


