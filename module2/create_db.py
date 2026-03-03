
import sqlite3
import os

def create_database():
    """
    Создает базу данных avtoservice.db со всеми необходимыми таблицами
    в 3 нормальной форме
    """
    
    conn = sqlite3.connect('avtoservice.db')
    cursor = conn.cursor()
    
    print("Создание таблиц базы данных...")
    
    # 1. Таблица users (пользователи)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        fio TEXT NOT NULL,
        phone TEXT,
        login TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    ''')
    print("✓ Таблица users создана")
    
    # 2. Таблица requests (заявки)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS requests (
        request_id INTEGER PRIMARY KEY,
        start_date TEXT NOT NULL,
        car_type TEXT NOT NULL,
        car_model TEXT NOT NULL,
        problem_description TEXT NOT NULL,
        request_status TEXT NOT NULL,
        completion_date TEXT,
        repair_parts TEXT,
        master_id INTEGER,
        client_id INTEGER NOT NULL,
        FOREIGN KEY (master_id) REFERENCES users(user_id),
        FOREIGN KEY (client_id) REFERENCES users(user_id)
    )
    ''')
    print("✓ Таблица requests создана")
    
    # 3. Таблица comments (комментарии)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        comment_id INTEGER PRIMARY KEY,
        message TEXT NOT NULL,
        master_id INTEGER NOT NULL,
        request_id INTEGER NOT NULL,
        FOREIGN KEY (master_id) REFERENCES users(user_id),
        FOREIGN KEY (request_id) REFERENCES requests(request_id)
    )
    ''')
    print("✓ Таблица comments создана")
    
    conn.commit()
    conn.close()
    print("\nБаза данных avtoservice.db успешно создана!")

if __name__ == "__main__":
    if os.path.exists('avtoservice.db'):
        os.remove('avtoservice.db')
        print("Старая база данных удалена")
    
    create_database()