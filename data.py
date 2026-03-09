from models import Request, Comment

requests = []
comments = []

users = [
    {"login": "login1", "password": "pass1", "name": "Саша", "role": "Менеджер"},
    {"login": "login2", "password": "pass2", "name": "Влад", "role": "Автомеханик"},
    {"login": "login3", "password": "pass3", "name": "Слава", "role": "Автомеханик"},
    {"login": "login4", "password": "pass4", "name": "Катя", "role": "Оператор"},
    {"login": "login5", "password": "pass5", "name": "Калыван", "role": "Оператор"},
    {"login": "login6", "password": "pass6", "name": "Клиент", "role": "Заказчик"},
    {"login": "login7", "password": "pass7", "name": "Елена", "role": "Менеджер качества"},
]

def load_data():

    r1 = Request()
    r1.id = 1
    r1.start_date = "2023-06-06"
    r1.car_type = "Легковая"
    r1.car_model = "Hyundai Avante"
    r1.problem = "Отказали тормоза"
    r1.status = "В процессе ремонта"
    r1.master_id = 2
    r1.client_name = "Ильина Тамара"
    r1.client_phone = "89219567841"
    requests.append(r1)
    
    r2 = Request()
    r2.id = 2
    r2.start_date = "2023-05-05"
    r2.car_type = "Легковая"
    r2.car_model = "Nissan 180SX"
    r2.problem = "Отказали тормоза"
    r2.status = "В процессе ремонта"
    r2.master_id = 3
    r2.client_name = "Елисеева Юлиана"
    r2.client_phone = "89219567842"
    requests.append(r2)
    
    r3 = Request()
    r3.id = 3
    r3.start_date = "2022-07-07"
    r3.car_type = "Легковая"
    r3.car_model = "Toyota 2000GT"
    r3.problem = "Пахнет бензином"
    r3.status = "Готова к выдаче"
    r3.end_date = "2023-01-01"
    r3.master_id = 3
    r3.client_name = "Никифорова Алиса"
    r3.client_phone = "89219567843"
    requests.append(r3)
    
    r4 = Request()
    r4.id = 4
    r4.start_date = "2023-08-02"
    r4.car_type = "Грузовая"
    r4.car_model = "Citroen Berlingo"
    r4.problem = "Руль плохо крутится"
    r4.status = "Новая заявка"
    r4.client_name = "Елисеева Юлиана"
    r4.client_phone = "89219567842"
    requests.append(r4)
    
    r5 = Request()
    r5.id = 5
    r5.start_date = "2023-08-02"
    r5.car_type = "Грузовая"
    r5.car_model = "УАЗ 2360"
    r5.problem = "Руль плохо крутится"
    r5.status = "Новая заявка"
    r5.client_name = "Никифорова Алиса"
    r5.client_phone = "89219567843"
    requests.append(r5)
    
    c1 = Comment()
    c1.id = 1
    c1.text = "Очень странно"
    c1.master_name = "Харитонова Мария"
    c1.request_id = 1
    comments.append(c1)
    
    c2 = Comment()
    c2.id = 2
    c2.text = "Будем разбираться"
    c2.master_name = "Марков Давид"
    c2.request_id = 2
    comments.append(c2)
    
    c3 = Comment()
    c3.id = 3
    c3.text = "Будем разбираться"
    c3.master_name = "Марков Давид"
    c3.request_id = 3
    comments.append(c3)