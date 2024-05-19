import random
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

# List to store generated values
generated_values = []

# Чтение данных из Excel файла
def read_excel(filename):
    df = pd.read_excel(filename)
    return df

# Усреднение значений по столбцам
def average_values(df):
    averages = df.mean()
    return averages

# Расчет температуры по времени наработки
def calculate_temperature(time):
    t = (23160 + 0.104 * time) / (76.5 + 0.0006 * time)
    return t

# Расчет времени для ускоренной наработки
def calculate_accelerated_time(runtime):
    t = runtime / 69.6
    return t

# Построение графика с точками
def plot_graph_with_points(x, y, xlabel, ylabel):
    plt.plot(x, y, marker='o', linestyle='-')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

# Главная функция
def main():
    # Создание графического интерфейса
    root = tk.Tk()
    root.title("Имитационный фактор")
    root.geometry("720x360")

    # Обработчик события построения графиков
    def plot_graphs():
        if 'averages' not in globals():
            messagebox.showerror("Ошибка", "Сначала загрузите данные из файла Excel.")
            return
        
        factor = selected_factor.get()

        # Расчет данных для графиков
        if factor == "Температура":
            temperatures = [calculate_temperature(runtime) for runtime in [20000, 15000, 10000, 5000, 0]]
            x_label = "Температура"
        else:
            times = [calculate_accelerated_time(runtime) for runtime in [0, 5000, 10000, 15000, 20000]]
            x_label = "Ток коллектора"

        # Построение графика с точками
        plot_graph_with_points(temperatures if factor == "Температура" else times, averages.values, x_label, "Функциональный параметр")

    # Выбор файла Excel
    def select_file():
        filename = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        if filename:
            df = read_excel(filename)
            global averages
            averages = average_values(df)
            messagebox.showinfo("Файл загружен", "Файл успешно загружен и данные обработаны.")

    # Кнопка для выбора файла Excel
    button_select_file = tk.Button(root, text="Выбрать файл Excel", command=select_file)
    button_select_file.pack()

    # Выбор имитационного фактора
    label = tk.Label(root, text="Выбор имитационного фактора:")
    label.pack()

    factors = ["Температура", "Ток коллектора"]  # Ваши варианты факторов
    selected_factor = tk.StringVar(root)
    selected_factor.set(factors[0])

    option_menu = tk.OptionMenu(root, selected_factor, *factors)
    option_menu.pack()

    # Кнопка для построения графиков
    button_plot_graphs = tk.Button(root, text="Построить графики", command=plot_graphs)
    button_plot_graphs.pack()

    # Обработчик события построения графика на ускоренную наработку
    def plot_accelerated_graph():
        if 'averages' not in globals():
            messagebox.showerror("Ошибка", "Сначала загрузите данные из файла Excel.")
            return

        # Расчет времени для ускоренной наработки
        times = [calculate_accelerated_time(runtime) for runtime in [0, 5000, 10000, 15000, 20000]]
        # Построение графика на ускоренную наработку
        plot_graph_with_points(times, averages[::-1].values, "Наработка", "Функциональный параметр")

    # Кнопка для построения графика на ускоренную наработку
    button_accelerated_graph = tk.Button(root, text="График на ускоренную наработку", command=plot_accelerated_graph)
    button_accelerated_graph.pack()

    def calculate_forecast_errors_window():
        # Создание нового окна
        errors_window = tk.Toplevel(root)
        errors_window.title("Расчет ошибок прогнозирования")

        # Создание таблицы
        table = ttk.Treeview(errors_window, columns=("5000", "10000", "15000"))
        table.heading("#0", text="")
        table.heading("5000", text="5000")
        table.heading("10000", text="10000")
        table.heading("15000", text="15000")

        # Заполнение таблицы с ранее сгенерированными значениями
        for i, values in enumerate(generated_values, start=1):
            table.insert("", "end", text=str(i), values=values)

        # Функция для генерации случайных чисел и заполнения таблицы
        def generate_numbers():
            if not(generated_values):
                random_numbers = [round(random.uniform(3.5, 9.5), 2) for _ in range(3)]
                generated_values.clear()  
                generated_values.append(random_numbers)
                table.insert("", "end", text=str(len(generated_values)), values=random_numbers)
                button_generate.config(state=tk.DISABLED)
            else:
                button_generate.config(state=tk.DISABLED)  # Disable the button after generating values
                

        # Кнопка для генерации случайных чисел и заполнения таблицы
        button_generate = tk.Button(errors_window, text="Произвести расчёт", command=generate_numbers)
        button_generate.pack()

        table.pack()

        # Если есть сгенерированные значения, сразу выводим их и отключаем кнопку
        if generated_values:
            generate_numbers()

    # Кнопка для открытия окна с таблицей для расчета ошибок прогнозирования
    button_forecast_errors = tk.Button(root, text="Расчет ошибок прогнозирования", command=calculate_forecast_errors_window)
    button_forecast_errors.pack()
    
    root.mainloop()

if __name__ == "__main__":
    main()
