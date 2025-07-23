import sqlite3
DB_name = 'finance.db'
def add_category(name):
    with sqlite3.connect(DB_name) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
            conn.commit()
        except sqlite3.IntegrityError:
            print('категория уже есть или произошла какая-то ошибка')

def update_category(old_name, new_name):
    with sqlite3.connect(DB_name) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE categories SET name = ? WHERE name = ?", (old_name, new_name))
            if cursor.rowcount == 0:
                print(f'ошибка категория {old_name} не найдена')
            else:
                print(f'окей, категория {old_name}  изменена на  {new_name}')
        except sqlite3.IntegrityError:
            print(f'ошибка {new_name} уже существует ')


def del_category(name):
    with sqlite3.connect(DB_name) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM categories  WHERE name = ? ", (name,))
        if cursor.rowcount == 0:
            print(f'ошибка, категория с именем {name} не найдена')
        else:
            print(f'категория {name} и все платежи к ней удалены') 

def get_all_category():
    with sqlite3.connect(DB_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT  id, name FROM categories ORDER BY name")
        return cursor.fetchall()
    
def get_category(category_name):
    with sqlite3.connect(DB_name) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id,name FROM categories WHERE name = ?',(category_name,))
        category = cursor.fetchone()
        #  return category
        if not category:
            #TODO 
            #сделать норм обработку ошибок 
            return []
        cursor.execute("""SELECT id,date,amount, type 
                       FROM payments
                        WHERE category_id = ?""" 
                       , (category[0],))
        payments = cursor.fetchone()
        return payments
        


    
# add_category('pipisi')
# add_category('kaki')
# print(get_all_category())
# print(get_category('kaki'))





