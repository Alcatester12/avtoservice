"""
import sqlite3

def print_results(title, results, headers):
    """Вывод результатов запроса"""
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)
    
    if not results:
        print("Нет данных")
        return
    
    # Вывод заголовков
    header_line = " | ".join(headers)
    print(header_line)
    print("-" * len(header_line))
    
    # Вывод строк
    for row in results:
        row_str = " | ".join(str(item) for item in row)
        print(row_str)
    
    print(f"\nВсего записей: {len(results)}")

def query1_all_requests(cursor):
    """Запрос 1: Все заявки с информацией о клиентах"""
    cursor.execute('''
    SELECT 
        r.request_id,
        r.start_date,
        r.car_model,
        r.problem_description,
        r.request_status,
        u.fio as client_name
    FROM requests r
    JOIN users u ON r.client_id = u.user_id
    ORDER BY r.request_id
    ''')
    results = cursor.fetchall()
    headers = ["ID", "Дата", "Модель", "Проблема", "Статус", "Клиент"]
    print_results("ЗАПРОС 1: Все заявки", results, headers)

def query2_requests_by_status(cursor):
    """Запрос 2: Количество заявок по статусам"""
    cursor.execute('''
    SELECT 
        request_status,
        COUNT(*) as count
    FROM requests
    GROUP BY request_status
    ORDER BY count DESC
    ''')
    results = cursor.fetchall()
    headers = ["Статус", "Количество"]
    print_results("ЗАПРОС 2: Заявки по статусам", results, headers)

def query3_masters_requests(cursor):
    """Запрос 3: Механики и их заявки"""
    cursor.execute('''
    SELECT 
        u.fio as master_name,
        COUNT(r.request_id) as requests_count
    FROM users u
    LEFT JOIN requests r ON u.user_id = r.master_id
    WHERE u.role = 'Автомеханик'
    GROUP BY u.fio
    ORDER BY requests_count DESC
    ''')
    results = cursor.fetchall()
    headers = ["Механик", "Количество заявок"]
    print_results("ЗАПРОС 3: Заявки по механикам", results, headers)

def query4_comments(cursor):
    """Запрос 4: Комментарии к заявкам"""
    cursor.execute('''
    SELECT 
        r.request_id,
        r.car_model,
        u.fio as master_name,
        c.message
    FROM comments c
    JOIN requests r ON c.request_id = r.request_id
    JOIN users u ON c.master_id = u.user_id
    ORDER BY r.request_id
    ''')
    results = cursor.fetchall()
    headers = ["ID заявки", "Модель", "Механик", "Комментарий"]
    print_results("ЗАПРОС 4: Комментарии", results, headers)

def query5_avg_time(cursor):
    """Запрос 5: Среднее время ремонта"""
    cursor.execute('''
    SELECT 
        COUNT(*) as total,
        AVG(
            julianday(completion_date) - julianday(start_date)
        ) as avg_days
    FROM requests
    WHERE completion_date IS NOT NULL
    ''')
    results = cursor.fetchall()
    headers = ["Всего завершено", "Среднее время (дней)"]
    
    # Округляем среднее время
    if results and results[0][1]:
        results = [(results[0][0], round(results[0][1], 1))]
    
    print_results("ЗАПРОС 5: Среднее время ремонта", results, headers)

def main():
    conn = sqlite3.connect('../avtoservice.db')
    cursor = conn.cursor()
    
    print("\n" + "=" * 80)
    print("ЗАПРОСЫ К БАЗЕ ДАННЫХ")
    print("=" * 80)
    
    query1_all_requests(cursor)
    query2_requests_by_status(cursor)
    query3_masters_requests(cursor)
    query4_comments(cursor)
    query5_avg_time(cursor)
    
    conn.close()

if __name__ == "__main__":
    main()