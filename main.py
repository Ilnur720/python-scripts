import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("500x500")
        self.history_file = "history.json"

        # Переменные настроек
        self.length_var = tk.IntVar(value=12)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_specials = tk.BooleanVar(value=True)

        self.setup_ui()
        self.load_history()

    def setup_ui(self):
        # Настройка параметров
        settings_frame = ttk.LabelFrame(self.root, text="Настройки пароля", padding=10)
        settings_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(settings_frame, text="Длина:").pack(side="left")
        self.length_slider = ttk.Scale(settings_frame, from_=4, to=32, variable=self.length_var, orient="horizontal")
        self.length_slider.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Label(settings_frame, textvariable=self.length_var).pack(side="left")

        options_frame = ttk.Frame(self.root, padding=10)
        options_frame.pack(fill="x")

        ttk.Checkbutton(options_frame, text="Цифры", variable=self.use_digits).pack(side="left")
        ttk.Checkbutton(options_frame, text="Буквы", variable=self.use_letters).pack(side="left")
        ttk.Checkbutton(options_frame, text="Спецсимволы", variable=self.use_specials).pack(side="left")

        # Кнопка генерации
        ttk.Button(self.root, text="Сгенерировать пароль", command=self.generate_password).pack(pady=10)

        # Поле вывода результата
        self.result_entry = ttk.Entry(self.root, font=("Courier", 14), justify="center")
        self.result_entry.pack(fill="x", padx=20, pady=5)

        # Таблица истории
        ttk.Label(self.root, text="История генераций:").pack(anchor="w", padx=10)
        self.tree = ttk.Treeview(self.root, columns=("Password"), show="headings")
        self.tree.heading("Password", text="Пароль")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def generate_password(self):
        chars = ""
        if self.use_letters.get(): chars += string.ascii_letters
        if self.use_digits.get(): chars += string.digits
        if self.use_specials.get(): chars += string.punctuation

        if not chars:
            messagebox.showwarning("Ошибка", "Выберите хотя бы один тип символов!")
            return

        length = self.length_var.get()
        password = "".join(random.choice(chars) for _ in range(length))

        self.result_entry.delete(0, tk.END)
        self.result_entry.insert(0, password)
        self.save_to_history(password)

    def save_to_history(self, password):
        self.tree.insert("", 0, values=(password,))

        history = []
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                history = json.load(f)

        history.append(password)
        with open(self.history_file, "w") as f:
            json.dump(history[-20:], f)  # Храним последние 20

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                history = json.load(f)
                for pwd in reversed(history):
                    self.tree.insert("", "end", values=(pwd,))


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
