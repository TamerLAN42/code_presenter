import tkinter as tk
import csv
import ast

title = "Презентатор обследований МСЭ"

# Создаем основное окно
root = tk.Tk()
root.title(title)
root.geometry("700x700")

# Создаем рамку для кнопок
button_frame = tk.Frame(root)
button_frame.grid(row=0, column=0, padx=10, pady=10)  # Размещаем рамку в первой строке и первом столбце

# Создаем текстовое поле для ввода
entry = tk.Entry(root, width=40)
entry.grid(row=0, column=1, padx=10, pady=10)  # Размещаем текстовое поле в первой строке и втором столбце

# Настраиваем растяжение для строки и колонки с полем вывода
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(2, weight=1)

# Создаем текстовое поле для вывода результатов
output_text = tk.Text(root, width=40, height=20)
output_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')  # Поле вывода на всю ширину

# Загружаем данные
codes = []
with open('mse_valid.csv', mode='r', newline='', encoding='utf-8') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        row['code'] = ast.literal_eval(row['code'])
        codes.append(row)

# Инициализируем пустой список для хранения подходящих обследований
match_obs = []
code_buffer = []     # Все введённые коды заносим в список. Потом пользователя лицом будем в это тыкать

# Функция для перевода на английскую раскладку
def transliterate(text):
    rus_to_eng = {
        'а': 'f', 'б': ',', 'в': 'd', 'г': 'u', 'д': 'l',
        'е': 't', 'ё': '`', 'ж': ';', 'з': 'p', 'и': 'b',
        'й': 'q', 'к': 'r', 'л': 'k', 'м': 'v', 'н': 'y',
        'о': 'j', 'п': 'g', 'р': 'h', 'с': 'c', 'т': 'n',
        'у': 'e', 'ф': 'a', 'х': '[', 'ц': 'w', 'ч': 'x',
        'ш': 'i', 'щ': 'o', 'ъ': ']', 'ы': 's', 'ь': 'm',
        'э': "'", 'ю': '.', 'я': 'z'
    }

    # Для поддержки заглавных букв добавляем их в словарь
    rus_to_eng.update({k.upper(): v.upper() for k, v in rus_to_eng.items()})

    # Трансформация текста
    transformed_text = ''.join(rus_to_eng.get(char, char) for char in text)
    return transformed_text


# Функция для вывода текста в графическое окно
def display_output(text):
    output_text.insert(tk.END, text + "\n")
    output_text.see(tk.END)  # Скроллим к последней строке


# Добавление названия в буфер. Код парсится, выводится кол-во совпадений в обследованиях
def action_add_code(event=None):
    global match_obs
    global code_buffer
    user_input = transliterate(entry.get().upper())
    entry.delete(0, tk.END)     # Чистим ввод

    # Ввод пустой строки расценивается как желание закончить ввод последовательности
    if user_input == '':
        action_get_output()
        return 0

    local_exams = [row['code'] for row in codes if row['mkb'] == user_input]      # Все обследования с тем-же кодом МКБ заносятся в список
    local_exams = list(sum(local_exams, []))

    display_output(f"Введенный код МКБ: {user_input}")
    display_output(f"Найдено обследований: {len(local_exams)}")
    match_obs.extend(local_exams)   # Выводим подходящее в глобальную переменную
    code_buffer.append(user_input)



# Вывод названий, очистка буфера сохраненных кодов МКБ
def action_get_output():
    global match_obs
    global code_buffer
    output_text.delete("1.0", tk.END)
    display_output(f"Учтённые коды МКБ:\n{code_buffer}\n")
    # Выводим каждое уникальное наименование в списке подходящих обследований
    for i in list(set(match_obs)):
        display_output(f"{i}")
    # Очищаем список подходящих обследований после вывода
    match_obs = []
    code_buffer = []
    # Очищаем поле для ввода текста
    entry.delete(0, tk.END)

# Спасибо tkinter за то, что вынуждает меня изобретать велосипед.
def copy_to_clipboard():
    root.clipboard_clear()  # Очищаем буфер обмена
    text = output_text.get("1.0", tk.END)  # Получаем весь текст из текстового поля
    root.clipboard_append(text)  # Добавляем текст в буфер обмена
    root.title("Текст скопирован!")
    root.after(1000, lambda: root.title(title))


# Функция для очистки поля вывода
def clear_output():
    global match_obs
    global code_buffer
    output_text.delete("1.0", tk.END)          # Очищаем все содержимое поля вывода
    entry.delete(0, tk.END)                     # Очищаем содержимое ввода
    match_obs = []                                  # Чистим подходящие обследования
    code_buffer = []
    root.title("Список кодов очищен")
    root.after(1000, lambda: root.title(title))


# Кнопочки. Просто кнопочки
button1 = tk.Button(button_frame, text="Дополнить список", command=action_add_code)
button1.grid(row=0, column=1, padx=20, pady=10)

button2 = tk.Button(button_frame, text="Вывести названия", command=action_get_output)
button2.grid(row=0, column=0, padx=20, pady=10)

button3 = tk.Button(button_frame, text="Копировать", command=copy_to_clipboard)
button3.grid(row=2, column=1, padx=20, pady=10)

button4 = tk.Button(button_frame, text="Очистить вывод", command=clear_output)
button4.grid(row=2, column=0, padx=20, pady=10)

# Привязываем клавишу "Enter" к функции on_first_button_click
root.bind('<Return>', action_add_code)

# Запускаем основной цикл программы
root.mainloop()
