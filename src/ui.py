#ui.py
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, Label, Button
import os
import shutil
from simulation import parallel_simulation
from visualisation import plot_results
from save_results import save_results_to_pdf
import numpy as np
from model import Population

RESULTS_DIR = "data"
TEMP_GRAPH_PATH = os.path.join(RESULTS_DIR, "temp_graph.png")

class SimulationApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Симуляція поширення вірусу")
        self.root.geometry("400x250")
        self.root.config(bg="#f4f4f4")
        self.center_window(self.root, 400, 250)
        self.results_saved = False
        self.susceptible = None
        self.infected = None
        self.recovered = None
        self.show_main_menu()

    def center_window(self, window, width, height):
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        window.geometry(f"{width}x{height}+{x}+{y}")

    def create_label(self, parent, text, font_size=10):
        label = tk.Label(parent, text=text, font=("Arial", font_size), bg="#f4f4f4")
        label.grid(padx=10, pady=10)  # Збільшені відступи для кращого вирівнювання
        return label

    def create_button(self, parent, text, command, font_size=10):
        button = tk.Button(parent, text=text, font=("Arial", font_size), command=command, width=20, height=1, 
                           bg="#4CAF50", fg="white", relief="solid", bd=2)
        button.grid(padx=10, pady=10)  # Збільшені відступи для кращого вирівнювання
        return button

    def create_entry(self, parent, default_value="", font_size=10):
        entry = tk.Entry(parent, font=("Arial", font_size), width=20, bd=2, relief="solid")
        entry.insert(0, default_value)
        entry.grid(padx=10, pady=5)
        return entry

    def show_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        main_menu_frame = tk.Frame(self.root, bg="#f4f4f4")
        main_menu_frame.grid(row=0, column=0, sticky="nsew")

        # Налаштовуємо вирівнювання для всіх рядів і колонок
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        main_menu_frame.grid_rowconfigure(0, weight=1)
        main_menu_frame.grid_columnconfigure(0, weight=1)

        # Розміщуємо лейбл та кнопки в центрі
        label = self.create_label(main_menu_frame, "Оберіть опцію:", 14)
        label.grid(row=0, column=0, sticky="nsew")

        button1 = self.create_button(main_menu_frame, "Створити новий тест", self.show_simulation_settings, 12)
        button1.grid(row=1, column=0, sticky="nsew")

        button2 = self.create_button(main_menu_frame, "Завантажити параметри з файлу", self.load_parameters, 12)
        button2.grid(row=2, column=0, sticky="nsew")

        button3 = self.create_button(main_menu_frame, "Вихід", self.root.quit, 12)
        button3.grid(row=3, column=0, sticky="nsew")

        # Встановлення розміру вікна назад на 400x250
        self.root.geometry("400x250")
        self.center_window(self.root, 400, 250)


    def get_population_input(self):
        # Запитуємо у користувача загальні параметри популяції
        total_population = int(self.population_entry.get())
    
        male_percentage = float(self.male_entry.get()) / 100
        female_percentage = float(self.female_entry.get()) / 100
        children_percentage = float(self.children_entry.get()) / 100
        young_adults_percentage = float(self.young_adults_entry.get()) / 100
        middle_age_percentage = float(self.middle_age_entry.get()) / 100
        senior_percentage = float(self.senior_entry.get()) / 100
    
        # Створюємо об'єкт Population
        population = Population(total_population)
    
        # Оновлюємо відсотки для кожної категорії
        population.male_percentage = male_percentage
        population.female_percentage = female_percentage
        population.children_percentage = children_percentage
        population.young_adults_percentage = young_adults_percentage
        population.middle_age_percentage = middle_age_percentage
        population.senior_percentage = senior_percentage
    
        # Розраховуємо кількість осіб в кожній категорії на основі відсотків
        population.males = total_population * male_percentage
        population.females = total_population * female_percentage
        population.children = total_population * children_percentage
        population.young_adults = total_population * young_adults_percentage
        population.middle_aged = total_population * middle_age_percentage
        population.senior = total_population * senior_percentage
    
        # Враховуємо, що загальна кількість осіб = сума всіх категорій
        population.total_population = population.males + population.females + population.children + population.young_adults + population.middle_aged + population.senior
    
        return population
    

    def load_parameters(self):
        file_path = filedialog.askopenfilename(title="Виберіть файл з параметрами", filetypes=[("Text files", "*.txt")])

        if not file_path:
            return  # Користувач скасував вибір файлу

        with open(file_path, 'r') as file:
            parameters = file.readlines()

        if len(parameters) < 4:
            messagebox.showerror("Помилка", "Файл має містити мінімум 4 рядки параметрів.")
            return

        # Переходимо на екран налаштувань симуляції, якщо ще не там
        self.show_simulation_settings()

        # Тепер можна безпечно заповнювати поля
        self.population_entry.delete(0, tk.END)
        self.population_entry.insert(0, parameters[0].strip())

        self.beta_entry.delete(0, tk.END)
        self.beta_entry.insert(0, parameters[1].strip())

        self.gamma_entry.delete(0, tk.END)
        self.gamma_entry.insert(0, parameters[2].strip())

        self.days_entry.delete(0, tk.END)
        self.days_entry.insert(0, parameters[3].strip())

        messagebox.showinfo("Готово", "Параметри завантажено успішно!")


    def show_simulation_settings(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Зміна розміру вікна на 400x750
        self.root.geometry("400x750")
        self.center_window(self.root, 400, 750)

        # Створюємо контейнер для сітки
        settings_frame = tk.Frame(self.root, bg="#f4f4f4")
        settings_frame.grid(pady=20)

        # Використовуємо grid для всіх елементів, включаючи кнопки
        # Розміщуємо лейбли та поля введення в декілька колонок

        self.create_label(settings_frame, "Назва експерименту:")
        self.experiment_name_entry = self.create_entry(settings_frame, "Test_Infection_X")
        self.experiment_name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.create_label(settings_frame, "Популяція:")
        self.population_entry = self.create_entry(settings_frame, "1000")
        self.population_entry.grid(row=1, column=1, padx=10, pady=5)

        # Додаємо нові поля для введення статі та вікових груп
        self.create_label(settings_frame, "Відсоток чоловіків:")
        self.male_entry = self.create_entry(settings_frame, "50")
        self.male_entry.grid(row=2, column=1, padx=10, pady=5)

        self.create_label(settings_frame, "Відсоток жінок:")
        self.female_entry = self.create_entry(settings_frame, "50")
        self.female_entry.grid(row=3, column=1, padx=10, pady=5)

        self.create_label(settings_frame, "Відсоток дітей:")
        self.children_entry = self.create_entry(settings_frame, "20")
        self.children_entry.grid(row=4, column=1, padx=10, pady=5)

        self.create_label(settings_frame, "Відсоток молодих людей:")
        self.young_adults_entry = self.create_entry(settings_frame, "30")
        self.young_adults_entry.grid(row=5, column=1, padx=10, pady=5)

        self.create_label(settings_frame, "Відсоток середнього віку:")
        self.middle_age_entry = self.create_entry(settings_frame, "30")
        self.middle_age_entry.grid(row=6, column=1, padx=10, pady=5)

        self.create_label(settings_frame, "Відсоток похилого віку:")
        self.senior_entry = self.create_entry(settings_frame, "20")
        self.senior_entry.grid(row=7, column=1, padx=10, pady=5)

        self.create_label(settings_frame, "Коеф. зараження (β):")
        self.beta_entry = self.create_entry(settings_frame, "0.3")
        self.beta_entry.grid(row=8, column=1, padx=10, pady=5)

        self.create_label(settings_frame, "Коеф. одужання (γ):")
        self.gamma_entry = self.create_entry(settings_frame, "0.1")
        self.gamma_entry.grid(row=9, column=1, padx=10, pady=5)

        self.create_label(settings_frame, "Кількість днів:")
        self.days_entry = self.create_entry(settings_frame, "100")
        self.days_entry.grid(row=10, column=1, padx=10, pady=5)

        # Використовуємо grid
        self.create_button(self.root, "Запустити симуляцію", self.run_simulation).grid(row=11, column=0, padx=10, pady=5, sticky="nsew")
        self.create_button(self.root, "Переглянути результати", self.show_results).grid(row=12, column=0, padx=10, pady=5, sticky="nsew")
        self.create_button(self.root, "Назад", self.show_main_menu).grid(row=13, column=0, padx=10, pady=5, sticky="nsew" )

        # Налаштовуємо сітку для контейнера
        settings_frame.grid_rowconfigure(0, weight=1)
        settings_frame.grid_rowconfigure(1, weight=1)
        settings_frame.grid_rowconfigure(2, weight=1)
        settings_frame.grid_rowconfigure(3, weight=1)
        settings_frame.grid_rowconfigure(4, weight=1)
        settings_frame.grid_rowconfigure(5, weight=1)
        settings_frame.grid_rowconfigure(6, weight=1)
        settings_frame.grid_rowconfigure(7, weight=1)
        settings_frame.grid_rowconfigure(8, weight=1)
        settings_frame.grid_rowconfigure(9, weight=1)
        settings_frame.grid_rowconfigure(10, weight=1)

        # Для стовпців теж можна налаштувати, якщо потрібно
        settings_frame.grid_columnconfigure(0, weight=1)
        settings_frame.grid_columnconfigure(1, weight=3)

    def run_simulation(self):
        experiment_name = self.experiment_name_entry.get()

        # Отримуємо популяцію через функцію get_population_input
        population = self.get_population_input()

        beta = float(self.beta_entry.get())
        gamma = float(self.gamma_entry.get())
        days = int(self.days_entry.get())

        # Виконуємо паралельну симуляцію з врахуванням популяції
        self.susceptible, self.infected, self.recovered = parallel_simulation(population, beta, gamma, days, 4)

        plot_results(self.susceptible, self.infected, self.recovered, save_path=TEMP_GRAPH_PATH)

        self.max_infected = np.max(self.infected)
        self.max_infected_day = np.argmax(self.infected)
        self.total_infected = np.sum(self.infected)

        self.results_saved = False
        messagebox.showinfo("Готово", "Симуляція завершена. Перегляньте результати.")

    def show_results(self):
        if not os.path.exists(TEMP_GRAPH_PATH):
            messagebox.showerror("Помилка", "Немає збережених результатів!")
            return

        result_window = Toplevel(self.root)
        result_window.title("Результати симуляції")
        result_window.config(bg="#f4f4f4")
        self.center_window(result_window, 1000, 850)

        # Розміщення заголовка
        self.create_label(result_window, "Результати симуляції:", 14)

        # Розміщення зображення
        img = tk.PhotoImage(file=TEMP_GRAPH_PATH)
        img_label = Label(result_window, image=img)
        img_label.image = img
        img_label.grid(row=1, column=0, padx=10, pady=10)  # Використовуємо grid замість pack

        # Формування текстового результату
        text_result = f"Experiment: {self.experiment_name_entry.get()}\n"
        text_result += f"Population: {self.population_entry.get()}, β: {self.beta_entry.get()}, γ: {self.gamma_entry.get()}, Days: {self.days_entry.get()}\n"
        text_result += f"Max infected: {int(self.max_infected)} on day {self.max_infected_day}\n"
        text_result += f"Total infected during the period: {int(self.total_infected)}"

        # Розміщення тексту результату
        self.create_label(result_window, text_result, 12)

        # Розміщення кнопки
        save_button = self.create_button(result_window, "Зберегти в PDF", lambda: self.save_results(result_window))
        save_button.grid(row=3, column=0, pady=10)  # Використовуємо grid для кнопки



    def save_results(self, result_window):
        experiment_name = self.experiment_name_entry.get()
        population = int(self.population_entry.get())
        beta = float(self.beta_entry.get())
        gamma = float(self.gamma_entry.get())
        days = int(self.days_entry.get())

        susceptible, infected, recovered = parallel_simulation(population, beta, gamma, days, 4)
        save_results_to_pdf(experiment_name, population, beta, gamma, days, susceptible, infected, recovered)
        self.results_saved = True
        messagebox.showinfo("Збережено", "Результати збережено у PDF.")

        result_window.destroy() 


    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def on_close(self):
        if not self.results_saved and os.path.exists(TEMP_GRAPH_PATH):
            os.remove(TEMP_GRAPH_PATH)
        self.root.destroy()

if __name__ == "__main__":
    app = SimulationApp()
    app.run()