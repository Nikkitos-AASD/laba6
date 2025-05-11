import tkinter as tk
from tkinter import filedialog, messagebox
import re

root = tk.Tk()
root.title("Редактор с РВ-поиском")
root.geometry("900x650")

# ==== Текстовое поле ====
text_area = tk.Text(root, wrap=tk.WORD)
text_area.pack(expand=1, fill=tk.BOTH)

# ==== Панель кнопок ====
toolbar = tk.Frame(root, bd=1, relief=tk.RAISED)
toolbar.pack(side=tk.TOP, fill=tk.X)

# ==== Список совпадений ====
results_list = tk.Listbox(root, height=7)
results_list.pack(fill=tk.X, padx=5, pady=5)

# ==== Функции ====

def show_task():
    messagebox.showinfo("Задание на лабораторную работу", 
        "Тема лабораторной работы: Реализация алгоритма поиска подстрок с помощью регулярных выражений.\n\n"
        "Цель: Реализовать алгоритм поиска подстрок, соответствующих заданным регулярным выражениям.\n\n"
        "Задание:\n"
        "— Построить РВ для паролей (латиница, цифры, символы).\n"
        "— Построить РВ для чисел (целые, с точкой или запятой).\n"
        "— Построить РВ для времени (ЧЧ:ММ:СС, 24-часовой формат).\n\n"
        "Встроить алгоритмы в текстовый редактор и выделять найденные подстроки."
    )

def highlight_matches(pattern):
    text_area.tag_remove("highlight", "1.0", tk.END)
    results_list.delete(0, tk.END)

    content = text_area.get("1.0", tk.END)
    matches = list(re.finditer(pattern, content))

    if not matches:
        messagebox.showinfo("Результат поиска", "Совпадений не найдено.")
        return

    for match in matches:
        start_pos = match.start()
        end_pos = match.end()
        matched_text = match.group()
        start_index = f"1.0 + {start_pos} chars"
        end_index = f"1.0 + {end_pos} chars"
        text_area.tag_add("highlight", start_index, end_index)
        results_list.insert(tk.END, f"{matched_text} (с {start_pos} по {end_pos})")

    text_area.tag_config("highlight", background="yellow")


def search_passwords():
    pattern = r"[A-Za-z0-9!@#$%^&*()_+=\-{}\[\]:;\"'<>,.?/\\|]{6,}"
    highlight_matches(pattern)

def search_numbers():
    pattern = r"[-+]?\d+(?:[.,]\d+)?"
    highlight_matches(pattern)

def search_time():
    pattern = r"\b(?:[01]?\d|2[0-3]):[0-5]?\d:[0-5]?\d\b"
    highlight_matches(pattern)

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, content)

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            content = text_area.get("1.0", tk.END)
            file.write(content)

# === Автомат через граф для времени ===

def is_valid_time_automaton_graph(s):
    if len(s) != 8 or s[2] != ':' or s[5] != ':':
        return False
    try:
        h1, h2 = int(s[0]), int(s[1])
        m1, m2 = int(s[3]), int(s[4])
        s1, s2 = int(s[6]), int(s[7])
    except ValueError:
        return False

    hh = h1 * 10 + h2
    mm = m1 * 10 + m2
    ss = s1 * 10 + s2

    return 0 <= hh <= 23 and 0 <= mm <= 59 and 0 <= ss <= 59

def find_all_valid_times(text):
    results = []
    for i in range(len(text) - 7):  # длина шаблона = 8 символов
        candidate = text[i:i+8]
        if is_valid_time_automaton_graph(candidate):
            results.append((candidate, i, i+8))
    return results

def search_times_automaton():
    text = text_area.get("1.0", tk.END)
    matches = find_all_valid_times(text)

    text_area.tag_remove("highlight", "1.0", tk.END)
    results_list.delete(0, tk.END)

    if not matches:
        messagebox.showinfo("Результат поиска", "Совпадений не найдено.")
        return

    for match_text, start, end in matches:
        start_index = f"1.0 + {start} chars"
        end_index = f"1.0 + {end} chars"
        text_area.tag_add("highlight", start_index, end_index)
        results_list.insert(tk.END, f"{match_text} (с {start} по {end})")

    text_area.tag_config("highlight", background="lightgreen")


# ==== Кнопки ====
tk.Button(toolbar, text="Задание ЛР", command=show_task).pack(side=tk.LEFT, padx=2, pady=2)
tk.Button(toolbar, text="Пароли", command=search_passwords).pack(side=tk.LEFT, padx=2, pady=2)
tk.Button(toolbar, text="Числа", command=search_numbers).pack(side=tk.LEFT, padx=2, pady=2)
tk.Button(toolbar, text="Время", command=search_time).pack(side=tk.LEFT, padx=2, pady=2)
tk.Button(root, text="Поиск времени (автомат)", command=search_times_automaton).pack(pady=5)

# ==== Меню ====
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Открыть", command=open_file)
file_menu.add_command(label="Сохранить", command=save_file)
menu_bar.add_cascade(label="Файл", menu=file_menu)
root.config(menu=menu_bar)

root.mainloop()
