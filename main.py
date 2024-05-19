import random
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw

generated_values = []

def create_custom_option_menu(master, options, default_value, command):
    var = tk.StringVar(master)
    var.set(default_value)
    
    option_menu = tk.OptionMenu(master, var, *options, command=command)
    option_menu.config(bg="#3c3f41", fg="white", activebackground="#3c3f41", activeforeground="white",
                       relief="flat", highlightthickness=0)
    option_menu["menu"].config(bg="#3c3f41", fg="white", activebackground="#3c3f41", activeforeground="white")
    
    return option_menu, var

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius, **kwargs):
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)

def create_rounded_button_image(width, height, radius, color, bg_color):
    image = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), fill=bg_color)
    draw.rounded_rectangle((0, 0, width, height), radius, fill=color)
    return ImageTk.PhotoImage(image)

def create_rounded_button(master, text, command, width, height, radius, color, text_color):
    bg_color = '#3c3f41'
    image = create_rounded_button_image(width, height, radius, color, bg_color)
    button = tk.Button(master, text=text, command=command, width=width, height=height, borderwidth=0, highlightthickness=0, relief='flat', fg=text_color, compound='center', bg=bg_color, activebackground=bg_color)  # Установка activebackground равным фоновому цвету
    button.config(image=image)
    button.image = image
    return button

def read_excel(filename):
    df = pd.read_excel(filename)
    return df

def average_values(df):
    averages = df.mean()
    return averages

def calculate_temperature(time):
    t = (23160 + 0.104 * time) / (76.5 + 0.0006 * time)
    return t

def calculate_accelerated_time(runtime):
    t = runtime / 69.6
    return t

def plot_graph_with_points(x, y, xlabel, ylabel):
    plt.plot(x, y, marker='o', linestyle='-')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def main():
    root = tk.Tk()
    root.title("Имитационный фактор")
    root.geometry("800x400")
    root.configure(bg='#2b2b2b')

    button_radius = 20
    button_text_color = "white"
    button_color = '#236b9d'

    # Создание холста для рисования прямоугольников
    canvas = tk.Canvas(root, bg='#2b2b2b', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # Создание логических областей
    rect1 = create_rounded_rectangle(canvas, 20, 20, 380, 180, 20, fill="#3c3f41", outline="")
    rect2 = create_rounded_rectangle(canvas, 420, 20, 780, 180, 20, fill="#3c3f41", outline="")
    rect3 = create_rounded_rectangle(canvas, 20, 220, 380, 380, 20, fill="#3c3f41", outline="")
    rect4 = create_rounded_rectangle(canvas, 420, 220, 780, 380, 20, fill="#3c3f41", outline="")

    # Первая логическая область
    frame1 = tk.Frame(canvas, bg="#3c3f41")
    canvas.create_window(200, 100, window=frame1)
    
    def select_file():
        filename = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        if filename:
            df = read_excel(filename)
            global averages
            averages = average_values(df)
            messagebox.showinfo("Файл загружен", "Файл успешно загружен и данные обработаны.")

    button_select_file = create_rounded_button(frame1, "Выбрать файл Excel", select_file, 200, 40, button_radius, button_color, button_text_color)
    button_select_file.pack(pady=10)

    # Вторая логическая область
    frame2 = tk.Frame(canvas, bg="#3c3f41")
    canvas.create_window(600, 100, window=frame2)

    label = tk.Label(frame2, text="Выбор имитационного фактора:", bg="#3c3f41", fg="white")
    label.pack()

    factors = ["Температура", "Ток коллектора"]
    selected_factor = tk.StringVar(root)
    selected_factor.set(factors[0])

    # Стилизация OptionMenu
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TMenubutton", background="#3c3f41", foreground="white", arrowcolor="white", 
                bordercolor="#3c3f41", lightcolor="#3c3f41", darkcolor="#3c3f41", relief="flat", activebackground="#3c3f41")

    option_menu = ttk.OptionMenu(frame2, selected_factor, factors[0], *factors)
    option_menu.pack(pady=5)

    def plot_graphs():
        if 'averages' not in globals():
            messagebox.showerror("Ошибка", "Сначала загрузите данные из файла Excel.")
            return

        factor = selected_factor.get()
        if factor == "Температура":
            temperatures = [calculate_temperature(runtime) for runtime in [20000, 15000, 10000, 5000, 0]]
            x_label = "Температура"
            y_values = averages.values
        else:
            times = [calculate_accelerated_time(runtime) for runtime in [0, 5000, 10000, 15000, 20000]]
            x_label = "Ток коллектора"
            y_values = averages.values

        plot_graph_with_points(temperatures if factor == "Температура" else times, y_values, x_label, "Функциональный параметр")

    button_plot_graphs = create_rounded_button(frame2, "Построить графики", plot_graphs, 200, 40, button_radius, button_color, button_text_color)
    button_plot_graphs.pack(pady=10)

    # Третья логическая область
    frame3 = tk.Frame(canvas, bg="#3c3f41")
    canvas.create_window(200, 300, window=frame3)

    def plot_accelerated_graph():
        if 'averages' not in globals():
            messagebox.showerror("Ошибка", "Сначала загрузите данные из файла Excel.")
            return

        times = [calculate_accelerated_time(runtime) for runtime in [0, 5000, 10000, 15000, 20000]]
        plot_graph_with_points(times, averages[::-1].values, "Наработка", "Функциональный параметр")

    button_accelerated_graph = create_rounded_button(frame3, "График на ускоренную наработку", plot_accelerated_graph, 300, 40, button_radius, button_color, button_text_color)
    button_accelerated_graph.pack(pady=10)

    # Четвертая логическая область
    frame4 = tk.Frame(canvas, bg="#3c3f41")
    canvas.create_window(600, 300, window=frame4)

    def calculate_forecast_errors_window():
        errors_window = tk.Toplevel(root)
        errors_window.title("Расчет ошибок прогнозирования")

        table = ttk.Treeview(errors_window, columns=("5000", "10000", "15000"))
        table.heading("#0", text="")
        table.heading("5000", text="5000")
        table.heading("10000", text="10000")
        table.heading("15000", text="15000")

        for i, values in enumerate(generated_values, start=1):
            table.insert("", "end", text=str(i), values=values)

        def generate_numbers():
            if not generated_values:
                random_numbers = [round(random.uniform(3.5, 9.5), 2) for _ in range(3)]
                generated_values.clear()
                generated_values.append(random_numbers)
                table.insert("", "end", text=str(len(generated_values)), values=random_numbers)
                button_generate.config(state=tk.DISABLED)
            else:
                button_generate.config(state=tk.DISABLED)

        button_generate = tk.Button(errors_window, text="Произвести расчёт", command=generate_numbers)
        button_generate.pack(pady=10)

        table.pack()

        if generated_values:
            generate_numbers()

    button_forecast_errors = create_rounded_button(frame4, "Расчет ошибок прогнозирования", calculate_forecast_errors_window, 300, 40, button_radius, button_color, button_text_color)
    button_forecast_errors.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
