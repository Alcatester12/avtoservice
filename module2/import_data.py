
import sqlite3
import csv

def import_users(cursor, filepath):
    """Импорт пользователей из inputDataUsers.txt"""
    print(f"Импорт пользователей из {filepath}...")
    count = 0
    
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)
        
        for row in reader:
            if len(row) >= 6:
                cursor.execute('''
                INSERT OR REPLACE INTO users (user_id, fio, phone, login, password, role)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (int(row[0]), row[1], row[2], row[3], row[4], row[5]))
                count += 1
    
    print(f"  ✓ Импортировано пользователей: {count}")
    return count

def import_requests(cursor, filepath):
    """Импорт заявок из inputDataRequests.txt"""
    print(f"Импорт заявок из {filepath}...")
    count = 0
    
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)
        
        for row in reader:
            if len(row) >= 10:
                master_id = int(row[8]) if row[8] and row[8].lower() != 'null' else None
                completion_date = row[6] if row[6] and row[6].lower() != 'null' else None
                
                cursor.execute('''
                INSERT OR REPLACE INTO requests 
                (request_id, start_date, car_type, car_model, problem_description, 
                 request_status, completion_date, repair_parts, master_id, client_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (int(row[0]), row[1], row[2], row[3], row[4], 
                      row[5], completion_date, row[7], master_id, int(row[9])))
                count += 1
    
    print(f"  ✓ Импортировано заявок: {count}")
    return count

def import_comments(cursor, filepath):
    """Импорт комментариев из inputDataComments.txt"""
    print(f"Импорт комментариев из {filepath}...")
    count = 0
    
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)
        
        for row in reader:
            if len(row) >= 4:
                cursor.execute('''
                INSERT OR REPLACE INTO comments (comment_id, message, master_id, request_id)
                VALUES (?, ?, ?, ?)
                ''', (int(row[0]), row[1], int(row[2]), int(row[3])))
                count += 1
    
    print(f"  ✓ Импортировано комментариев: {count}")
    return count

def main():
    conn = sqlite3.connect('avtoservice.db')
    cursor = conn.cursor()
    
    print("=" * 50)
    print("ИМПОРТ ДАННЫХ В БАЗУ ДАННЫХ")
    print("=" * 50)
    
    # Файлы находятся в родительской папке (на уровень выше)
    users_file = "../inputDataUsers.txt"
    requests_file = "../inputDataRequests.txt"
    comments_file = "../inputDataComments.txt"
    
    total_users = import_users(cursor, users_file)
    total_requests = import_requests(cursor, requests_file)
    total_comments = import_comments(cursor, comments_file)
    
    conn.commit()
    
    print("\n" + "=" * 50)
    print("ИТОГИ ИМПОРТА:")
    print(f"  Пользователей: {total_users}")
    print(f"  Заявок: {total_requests}")
    print(f"  Комментариев: {total_comments}")
    print("=" * 50)
    
    conn.close()

if __name__ == "__main__":
    main()