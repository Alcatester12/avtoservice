class Request:
    def __init__(self):
        self.id = 0
        self.start_date = ""
        self.car_type = ""
        self.car_model = ""
        self.problem = ""
        self.status = "Новая заявка"
        self.end_date = ""
        self.parts = ""
        self.master_id = 0
        self.client_name = ""
        self.client_phone = ""

class Comment:
    def __init__(self):
        self.id = 0
        self.text = ""
        self.master_name = ""
        self.request_id = 0