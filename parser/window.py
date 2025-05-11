import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Button, Label, Entry
from main import start_parsing

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Меню")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.filename = None
        self.database_host = None
        self.db_properties = {}

        self.init_main_menu()

    def init_main_menu(self):
        buttons = [
            ("Открыть Excel файл", self.open_file),
            ("Спарсить Excel файл", self.parse_excel),
            ("Подключиться к базе", self.admin_config)
        ]

        for i, (text, command) in enumerate(buttons):
            btn = Button(
                self.root,
                text=text,
                command=command,
                style="TButton",
            )
            btn.place(x=100, y=30 + i * 50, width=200, height=30)

    def open_file(self):
        filetypes = [("Excel файл", "*.xlsx")]
        self.filename = filedialog.askopenfilename(
            title="Выберите Excel файл", filetypes=filetypes
        )
        if self.filename:
            messagebox.showinfo("Файл выбран", f"Выбранный файл: {self.filename}")
        else:
            messagebox.showwarning("Нет файла", "Файл не выбран")

    def parse_excel(self):
        if not self.filename:
            messagebox.showerror("ОШИБКА", " Выбран не Excel - файл.")
            return

        try:
            print(f"Parsing file: {self.filename}")
            start_parsing(self.filename, self.return_connection_string())
            #messagebox.showinfo("Успешно", "Файл успешно спарсен")
            messagebox.showerror("Ошибка", f"Ошибка парсинга файла")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка парсинга файла: {e}")

    def configure_db_connection(self):
        config_window = tk.Toplevel(self.root)
        config_window.title("Database Connection")
        config_window.geometry("300x300")
        config_window.resizable(False, False)

        Label(config_window, text="Postgres host:").place(x=20, y=30)
        url_entry = Entry(config_window, width=25)
        url_entry.place(x=140, y=30)
        url_entry.insert(0, "localhost")

        Label(config_window, text="Username:").place(x=20, y=80)
        user_entry = Entry(config_window, width=25)
        user_entry.place(x=140, y=80)
        user_entry.insert(0, "postgres")

        Label(config_window, text="Password:").place(x=20, y=130)
        password_entry = Entry(config_window, width=25, show="*")
        password_entry.place(x=140, y=130)
        password_entry.insert(0, "ф")

        Label(config_window, text="Database:").place(x=20, y=130)
        database_entry = Entry(config_window, width=25, show="*")
        database_entry.place(x=140, y=130)
        database_entry.insert(0, "123456")

        def submit():
            self.database_host = url_entry.get()
            self.db_properties = {
                "user": user_entry.get(),
                "password": password_entry.get(),
                "database": database_entry.get()
            }
            config_window.destroy()
            messagebox.showinfo("Успешно", "Конфигурация базы данных обновлена")

        Button(
            config_window,
            text="Submit",
            command=submit,
        ).place(x=100, y=200, width=100, height=30)

    def admin_config(self):
        self.db_properties = {
            "user": "postgres",
            "password": "123456",
            "database": "postgres"
        }
        self.database_host = "localhost"
        messagebox.showinfo("Подключение", "Вход в базу совершен")
    
    def return_connection_string(self):
        print(f"host='{self.database_host}' dbname='{self.db_properties["database"]}' user='{self.db_properties["user"]}' password='{self.db_properties["password"]}'")
        return f"host='{self.database_host}' dbname='{self.db_properties["database"]}' user='{self.db_properties["user"]}' password='{self.db_properties["password"]}'"

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()