import tkinter as tk
from tkinter import messagebox
import json
import random
import datetime


class RandomTaskGenerator:
    """Генератор случайных задач."""

    TASK_TYPES = ["учёба", "спорт", "работа"]
    HISTORY_FILE = "tasks_history.json"

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("650x800")

        self.tasks = []
        self.history = []

        self._setup_ui()
        self._load_data()
        if not self.tasks:
            self._load_default_tasks()


    def _setup_ui(self):
        """Настройка интерфейса."""
        tk.Label(self.root, text="Генератор случайных задач", font="Arial 18 bold").pack(pady=10)

        # Добавление задачи
        tk.LabelFrame(self.root, text="Добавить задачу", font="Arial 12").pack(pady=5, padx=15, fill="x")

        tk.Label(self.root, text="Название:").pack()
        self.name_entry = tk.Entry(self.root, font="Arial 12", width=40)
        self.name_entry.pack(pady=3)

        tk.Label(self.root, text="Тип:").pack()
        self.type_var = tk.StringVar(value=self.TASK_TYPES[0])
        tk.OptionMenu(self.root, self.type_var, *self.TASK_TYPES).pack(pady=3)

        tk.Button(self.root, text="Добавить", bg="#4CAF50", fg="white",
                 command=self._add_task).pack(pady=8)

        # Управление задачами
        tk.Label(self.root, text="Список задач", font="Arial 12 bold").pack(pady=5)

        tasks_frame = tk.Frame(self.root)
        tasks_frame.pack(padx=15, fill="both", expand=True)

        self.tasks_listbox = tk.Listbox(tasks_frame, font="Arial 12", height=10)
        self.tasks_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(tasks_frame)
        scrollbar.pack(side="right", fill="y")
        self.tasks_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tasks_listbox.yview)

        tk.Button(self.root, text="Удалить выбранное", bg="#f44336", fg="white",
                 command=self._delete_task).pack(pady=5)

        # Генерация
        tk.LabelFrame(self.root, text="Генерация", font="Arial 12").pack(pady=10, padx=15, fill="x")

        self.filter_var = tk.StringVar(value="Все")
        tk.OptionMenu(self.root, self.filter_var, "Все", *self.TASK_TYPES).pack(pady=5)

        tk.Button(self.root, text="Сгенерировать", font="Arial 14 bold", bg="#FF9800",
                 fg="white", command=self._generate_task).pack(pady=8)

        self.result_label = tk.Label(self.root, text="Нажмите кнопку", font="Arial 14", fg="blue")
        self.result_label.pack(pady=5)

        # История
        tk.Label(self.root, text="История", font="Arial 12 bold").pack(pady=5)

        hist_frame = tk.Frame(self.root)
        hist_frame.pack(padx=15, fill="both", expand=True)

        self.history_listbox = tk.Listbox(hist_frame, font="Arial 11", height=8)
        self.history_listbox.pack(side="left", fill="both", expand=True)

        hist_scrollbar = tk.Scrollbar(hist_frame)
        hist_scrollbar.pack(side="right", fill="y")
        self.history_listbox.config(yscrollcommand=hist_scrollbar.set)
        hist_scrollbar.config(command=self.history_listbox.yview)

        tk.Button(self.root, text="Очистить историю", bg="#FF5722", fg="white",
                 command=self._clear_history).pack(pady=5)


    def _load_data(self):
        """Загрузка из JSON."""
        try:
            with open(self.HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.tasks = data.get("tasks", [])
                self.history = data.get("history", [])
            self._update_listboxes()
        except:
            pass


    def _save_data(self):
        """Сохранение в JSON."""
        with open(self.HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump({"tasks": self.tasks, "history": self.history}, f,
                     ensure_ascii=False, indent=2)


    def _load_default_tasks(self):
        """Загрузка стандартных задач."""
        self.tasks = [
            {"name": "Прочитать статью", "type": "учёба"},
            {"name": "Сделать зарядку", "type": "спорт"},
            {"name": "Написать отчёт", "type": "работа"},
            {"name": "Решить задачи", "type": "учёба"},
            {"name": "Пробежка 5 км", "type": "спорт"},
            {"name": "Провести совещание", "type": "работа"},
            {"name": "Выучить новые слова", "type": "учёба"},
            {"name": "Отжимания 50 раз", "type": "спорт"},
            {"name": "Ответить на письма", "type": "работа"}
        ]
        self._update_listboxes()
        self._save_data()


    def _add_task(self):
        """Добавление задачи."""
        name = self.name_entry.get().strip()
        if name:
            self.tasks.append({"name": name, "type": self.type_var.get()})
            self.name_entry.delete(0, tk.END)
            self._update_listboxes()
            self._save_data()
        else:
            messagebox.showwarning("Ошибка", "Введите название!")


    def _delete_task(self):
        """Удаление задачи."""
        selected = self.tasks_listbox.curselection()
        if selected:
            del self.tasks[selected[0]]
            self._update_listboxes()
            self._save_data()


    def _generate_task(self):
        """Генерация случайной задачи."""
        filter_type = self.filter_var.get()
        available = self.tasks if filter_type == "Все" else [t for t in self.tasks if t["type"] == filter_type]

        if not available:
            messagebox.showwarning("Ошибка", "Нет задач!")
            return

        task = random.choice(available)
        text = f"{task['name']} [{task['type']}]"
        time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

        self.history.append(f"{time} - {text}")
        self.result_label.config(text=text)
        self._update_listboxes()
        self._save_data()


    def _clear_history(self):
        """Очистка истории."""
        if messagebox.askyesno("Подтверждение", "Очистить историю?"):
            self.history.clear()
            self._update_listboxes()
            self._save_data()


    def _update_listboxes(self):
        """Обновление списков."""
        self.tasks_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.tasks_listbox.insert(tk.END, f"{task['name']} ({task['type']})")

        self.history_listbox.delete(0, tk.END)
        for entry in reversed(self.history):
            self.history_listbox.insert(tk.END, entry)


if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app._save_data(), root.destroy()))
    root.mainloop()
