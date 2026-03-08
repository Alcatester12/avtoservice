import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from models import Request, Comment
from data import requests, users, comments, load_data
import qrcode
from io import BytesIO
from PIL import Image, ImageTk

class App:
    def __init__(self):
        load_data()
        self.current_user = None
        self.window = tk.Tk()
        self.window.title("Автосервис - Учет заявок")
        self.window.geometry("800x600")
        self.show_login()
        self.window.mainloop()

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_window()
        frame = tk.Frame(self.window)
        frame.pack(expand=True)
        tk.Label(frame, text="ВХОД В СИСТЕМУ", font=("Arial", 16)).pack(pady=20)
        tk.Label(frame, text="Логин:").pack()
        self.login_entry = tk.Entry(frame)
        self.login_entry.pack(pady=5)
        tk.Label(frame, text="Пароль:").pack()
        self.pass_entry = tk.Entry(frame, show="*")
        self.pass_entry.pack(pady=5)
        tk.Button(frame, text="Войти", command=self.try_login).pack(pady=20)

    def try_login(self):
        for user in users:
            if user["login"] == self.login_entry.get() and user["password"] == self.pass_entry.get():
                self.current_user = user
                self.show_main_menu()
                return
        messagebox.showerror("Ошибка", "Неверный логин или пароль")

    def show_main_menu(self):
        self.clear_window()
        tk.Label(self.window, text="ГЛАВНОЕ МЕНЮ", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.window, text=f"{self.current_user['name']} ({self.current_user['role']})").pack()
        buttons = [
            ("Все заявки", self.show_all_requests),
            ("Новая заявка", self.add_request),
            ("Поиск", self.show_search),
            ("Статистика", self.show_stats)
        ]
        if self.current_user["role"] == "Автомеханик":
            buttons.insert(3, ("Мои заявки", self.show_my_requests))
        for text, cmd in buttons:
            tk.Button(self.window, text=text, width=20, command=cmd).pack(pady=5)
        tk.Button(self.window, text="Выход", width=20, command=self.window.quit).pack(pady=20)

    def show_requests_list(self, title, req_list):
        self.clear_window()
        tk.Button(self.window, text="← Назад", command=self.show_main_menu).pack(anchor="w", pady=5)
        tk.Label(self.window, text=title, font=("Arial", 14)).pack(pady=10)
        if not req_list:
            tk.Label(self.window, text="Нет заявок").pack()
            return
        frame = tk.Frame(self.window)
        frame.pack(fill="both", expand=True, padx=10)
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        self.listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set)
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)
        for req in req_list:
            self.listbox.insert("end", f"ID: {req.id} | {req.start_date} | {req.car_model} | {req.status}")
        self.current_req_list = req_list
        tk.Button(self.window, text="Просмотреть", command=self.show_selected_request).pack(pady=10)

    def show_all_requests(self):
        self.show_requests_list("ВСЕ ЗАЯВКИ", requests)

    def show_my_requests(self):
        my_reqs = [r for r in requests if r.master_id == self.current_user.get("id")]
        self.show_requests_list("МОИ ЗАЯВКИ", my_reqs)

    def show_selected_request(self):
        sel = self.listbox.curselection()
        if sel:
            self.show_request_details(self.current_req_list[sel[0]])

    def show_request_details(self, req):
        win = tk.Toplevel(self.window)
        win.title(f"Заявка №{req.id}")
        win.geometry("500x500")
        text = tk.Text(win, wrap="word")
        text.pack(fill="both", expand=True, padx=10, pady=10)
        text.insert("end", f"ЗАЯВКА №{req.id}\n")
        text.insert("end", f"Дата: {req.start_date}\n")
        text.insert("end", f"Авто: {req.car_type} {req.car_model}\n")
        text.insert("end", f"Проблема: {req.problem}\n")
        text.insert("end", f"Статус: {req.status}\n")
        text.insert("end", f"Клиент: {req.client_name}, {req.client_phone}\n")
        if req.master_id:
            master = next((u for u in users if u.get("id") == req.master_id), {})
            text.insert("end", f"Механик: {master.get('name', 'Неизвестно')}\n")
        if req.parts:
            text.insert("end", f"Запчасти: {req.parts}\n")
        text.insert("end", "\nКОММЕНТАРИИ:\n")
        comms = [c for c in comments if c.request_id == req.id]
        if comms:
            for c in comms:
                text.insert("end", f"{c.master_name}: {c.text}\n")
        else:
            text.insert("end", "Нет комментариев\n")
            text.config(state="disabled")
        frame = tk.Frame(win)
        frame.pack(pady=10)
        if self.current_user["role"] == "Автомеханик":
            tk.Button(frame, text="Изменить статус", command=lambda: self.change_status(req)).pack(side="left", padx=5)
            tk.Button(frame, text="Добавить запчасти", command=lambda: self.add_parts(req)).pack(side="left", padx=5)
            tk.Button(frame, text="Комментарий", command=lambda: self.add_comment(req)).pack(side="left", padx=5)
        elif self.current_user["role"] == "Менеджер качества":
            tk.Button(frame, text="Продлить срок", command=lambda: self.extend_deadline(req)).pack(side="left", padx=5)
            tk.Button(frame, text="Привлечь механика", command=lambda: self.assign_additional_mechanic(req)).pack(side="left", padx=5)
            tk.Button(frame, text="QR-код отзыва", command=lambda: self.show_qr_code(req)).pack(side="left", padx=5)
        elif self.current_user["role"] in ["Оператор", "Менеджер"] and not req.master_id:
            tk.Button(frame, text="Назначить механика", command=lambda: self.assign_master(req)).pack(pady=10)

    def add_comment_system(self, req, text):
        c = Comment()
        c.id = len(comments) + 1
        c.text = text
        c.master_name = self.current_user["name"]
        c.request_id = req.id
        comments.append(c)

    def change_status(self, req):
        win = tk.Toplevel(self.window)
        win.title("Изменить статус")
        win.geometry("300x250")
        tk.Label(win, text=f"Заявка №{req.id}").pack(pady=10)
        statuses = ["Новая заявка", "В процессе ремонта", "Ожидание запчастей", "Готова к выдаче", "Завершена"]
        var = tk.StringVar()
        for s in statuses:
            tk.Radiobutton(win, text=s, variable=var, value=s).pack(anchor="w", padx=20)
        def save():
            if var.get():
                req.status = var.get()
                if var.get() == "Завершена":
                    req.end_date = datetime.datetime.now().strftime("%Y-%m-%d")
                self.add_comment_system(req, f"Статус изменен на: {var.get()}")
                messagebox.showinfo("Успех", "Статус изменен")
                win.destroy()
        tk.Button(win, text="Сохранить", command=save).pack(pady=20)

    def add_parts(self, req):
        win = tk.Toplevel(self.window)
        win.title("Добавить запчасти")
        win.geometry("300x150")
        tk.Label(win, text=f"Заявка №{req.id}").pack(pady=10)
        entry = tk.Entry(win, width=40)
        entry.pack(pady=10)
        def save():
            if entry.get():
                req.parts = (req.parts + "; " + entry.get()) if req.parts else entry.get()
                self.add_comment_system(req, f"Добавлены запчасти: {entry.get()}")
                messagebox.showinfo("Успех", "Запчасти добавлены")
                win.destroy()
        tk.Button(win, text="Добавить", command=save).pack()

    def add_comment(self, req):
        win = tk.Toplevel(self.window)
        win.title("Добавить комментарий")
        win.geometry("300x150")
        tk.Label(win, text=f"Заявка №{req.id}").pack(pady=10)
        entry = tk.Entry(win, width=40)
        entry.pack(pady=10)
        def save():
            if entry.get():
                self.add_comment_system(req, entry.get())
                messagebox.showinfo("Успех", "Комментарий добавлен")
                win.destroy()
        tk.Button(win, text="Добавить", command=save).pack()

    def assign_master(self, req):
        win = tk.Toplevel(self.window)
        win.title("Назначить механика")
        win.geometry("300x200")
        tk.Label(win, text=f"Заявка №{req.id}").pack(pady=10)
        masters = [u for u in users if u["role"] == "Автомеханик"]
        var = tk.StringVar()
        for m in masters:
            tk.Radiobutton(win, text=m['name'], variable=var, value=m.get("id", 0)).pack(anchor="w", padx=20)
        def save():
            try:
                req.master_id = int(var.get())
                self.add_comment_system(req, "Назначен механик")
                messagebox.showinfo("Успех", "Механик назначен")
                win.destroy()
            except:
                messagebox.showerror("Ошибка", "Выберите механика")
        tk.Button(win, text="Назначить", command=save).pack(pady=20)

    def extend_deadline(self, req):
        """Продление срока заявки (для менеджера качества)"""
        win = tk.Toplevel(self.window)
        win.title("Продлить срок")
        win.geometry("300x200")
        
        tk.Label(win, text=f"Заявка №{req.id}").pack(pady=10)
        tk.Label(win, text=f"Текущая дата: {req.end_date or 'не указана'}").pack()
        
        tk.Label(win, text="Новая дата (ГГГГ-ММ-ДД):").pack()
        entry = tk.Entry(win)
        entry.pack(pady=5)
        
        def save():
            new_date = entry.get()
            if new_date:
                req.end_date = new_date
                self.add_comment_system(req, f"Срок продлён до {new_date} (менеджер качества)")
                messagebox.showinfo("Успех", "Срок изменён")
                win.destroy()
        
        tk.Button(win, text="Сохранить", command=save).pack(pady=10)

    def assign_additional_mechanic(self, req):
        """Привлечь дополнительного механика (менеджер качества)"""
        win = tk.Toplevel(self.window)
        win.title("Привлечь механика")
        win.geometry("300x250")
        
        tk.Label(win, text=f"Заявка №{req.id}").pack(pady=10)
        
        mechanics = [u for u in users if u["role"] == "Автомеханик"]
        var = tk.StringVar()
        
        for m in mechanics:
            tk.Radiobutton(win, text=m['name'], variable=var, value=m['name']).pack(anchor="w", padx=20)
        
        def save():
            mech_name = var.get()
            if mech_name:
                self.add_comment_system(req, f"Привлечён механик: {mech_name}")
                messagebox.showinfo("Успех", f"Механик {mech_name} привлечён")
                win.destroy()
        
        tk.Button(win, text="Привлечь", command=save).pack(pady=20)

    def show_qr_code(self, req):
        """Показать QR-код с отзывом"""
        url = "https://docs.google.com/forms/d/e/1FAIpQLSdhZcExx6LSIXxk0ub55mSu-WIh23WYdGG9HY5EZhLDo7P8eA/viewform"
        
        qr = qrcode.make(url)
        
        img_bytes = BytesIO()
        qr.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        pil_img = Image.open(img_bytes)
        img_tk = ImageTk.PhotoImage(pil_img)
        
        win = tk.Toplevel(self.window)
        win.title("QR-код для отзыва")
        win.geometry("300x350")
        
        tk.Label(win, text="Оцените качество работы").pack(pady=10)
        
        label_img = tk.Label(win, image=img_tk)
        label_img.image = img_tk
        label_img.pack(pady=10)
        
        tk.Label(win, text="Отсканируйте QR-код", font=("Arial", 10)).pack()
        
        tk.Button(win, text="Закрыть", command=win.destroy).pack(pady=10)

if __name__ == "__main__":
    App()