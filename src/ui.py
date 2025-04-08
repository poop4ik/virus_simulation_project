# ui.py
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, Label, Button
import os
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
        self.root.geometry("400x750")
        self.root.config(bg="#f4f4f4")
        self.center_window(self.root, 400, 750)
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
        self.center_window(self.root, 400, 900)
    
        # Створюємо контейнер для сітки
        settings_frame = tk.Frame(self.root, bg="#f4f4f4")
        settings_frame.grid(pady=20)
    
        # Використовуємо grid для всіх елементів, включаючи кнопки
        self.create_label(settings_frame, "Назва експерименту:")
        self.experiment_name_entry = self.create_entry(settings_frame, "Test_Infection_X")
        self.experiment_name_entry.grid(row=0, column=1, padx=10, pady=5)
    
        self.create_label(settings_frame, "Популяція:")
        self.population_entry = self.create_entry(settings_frame, "1000")
        self.population_entry.grid(row=1, column=1, padx=10, pady=5)
    
        # Додаємо нові поля для введення статі та вікових груп
        self.create_label(settings_frame, "Відсоток чоловіків:")
        self.male_entry = self.create_entry(settings_frame, "60")
        self.male_entry.grid(row=2, column=1, padx=10, pady=5)

        self.create_label(settings_frame, "Відсоток жінок:")
        self.female_entry = self.create_entry(settings_frame, "40")
        self.female_entry.grid(row=3, column=1, padx=10, pady=5)

        self.create_label(settings_frame, "Відсоток дітей (0-14 років):")
        self.children_entry = self.create_entry(settings_frame, "20")
        self.children_entry.grid(row=4, column=1, padx=10, pady=5)

        self.create_label(settings_frame, "Відсоток молодих людей (15-34 роки):")
        self.young_adults_entry = self.create_entry(settings_frame, "35")
        self.young_adults_entry.grid(row=5, column=1, padx=10, pady=5)

        self.create_label(settings_frame, "Відсоток середнього віку (35-64 роки):")
        self.middle_age_entry = self.create_entry(settings_frame, "25")
        self.middle_age_entry.grid(row=6, column=1, padx=10, pady=5)

        self.create_label(settings_frame, "Відсоток похилого віку (65+ років):")
        self.senior_entry = self.create_entry(settings_frame, "20")
        self.senior_entry.grid(row=7, column=1, padx=10, pady=5)

        # Додаємо коефіцієнти зараження та одужання
        self.create_label(settings_frame, "Коеф. зараження (β):")
        self.beta_entry = self.create_entry(settings_frame, "0.4")
        self.beta_entry.grid(row=8, column=1, padx=10, pady=5)

        self.create_label(settings_frame, "Коеф. одужання (γ):")
        self.gamma_entry = self.create_entry(settings_frame, "0.1")
        self.gamma_entry.grid(row=9, column=1, padx=10, pady=5)

        self.create_label(settings_frame, "Кількість днів:")
        self.days_entry = self.create_entry(settings_frame, "100")
        self.days_entry.grid(row=10, column=1, padx=10, pady=5)

        # Додаємо нові поля для коефіцієнтів летальності для кожної групи
        self.create_label(settings_frame, "Летальність дітей (%):")
        self.death_rate_children_entry = self.create_entry(settings_frame, "8")  # Значення за замовчуванням
        self.death_rate_children_entry.grid(row=11, column=1, padx=10, pady=5)

        self.create_label(settings_frame, "Летальності молодих (%):")
        self.death_rate_young_adults_entry = self.create_entry(settings_frame, "5")
        self.death_rate_young_adults_entry.grid(row=12, column=1, padx=10, pady=5)

        self.create_label(settings_frame, "Летальність середнього віку (%):")
        self.death_rate_middle_age_entry = self.create_entry(settings_frame, "6")
        self.death_rate_middle_age_entry.grid(row=13, column=1, padx=10, pady=5)

        self.create_label(settings_frame, "Летальність похилого віку (%):")
        self.death_rate_senior_entry = self.create_entry(settings_frame, "10")
        self.death_rate_senior_entry.grid(row=14, column=1, padx=10, pady=5)

        self.create_label(settings_frame, "Смертність чоловіків (%):")
        self.male_mortality_entry = self.create_entry(settings_frame, "8")
        self.male_mortality_entry.grid(row=15, column=1, padx=10, pady=5)

        self.create_label(settings_frame, "Смертність жінок (%):")
        self.female_mortality_entry = self.create_entry(settings_frame, "6")
        self.female_mortality_entry.grid(row=16, column=1, padx=10, pady=5)


        self.create_label(settings_frame, "Вакцинація (%)")
        self.vaccine_percent_entry =self.create_entry(settings_frame, "20")
        self.vaccine_percent_entry.grid(row=17, column=1, padx=10, pady=5)

        self.create_label(settings_frame, "Карантин (%)")
        self.quarantine_percent_entry = self.create_entry(settings_frame, "20")
        self.quarantine_percent_entry.grid(row=18, column=1, padx=10, pady=5)

        # Додаємо поля для зниження інфікування та смертності через вакцинацію та карантин
        self.create_label(settings_frame, "Зниження інфікування вакцинацією (%):")
        self.vaccine_infection_reduction_entry = self.create_entry(settings_frame, "60")
        self.vaccine_infection_reduction_entry.grid(row=19, column=1, padx=10, pady=5)

        self.create_label(settings_frame, "Зниження смертності вакцинацією (%):")
        self.vaccine_mortality_reduction_entry = self.create_entry(settings_frame, "50")
        self.vaccine_mortality_reduction_entry.grid(row=20, column=1, padx=10, pady=5)

        self.create_label(settings_frame, "Зниження інфікування карантином (%):")
        self.quarantine_infection_reduction_entry = self.create_entry(settings_frame, "70")
        self.quarantine_infection_reduction_entry.grid(row=21, column=1, padx=10, pady=5)

        self.create_label(settings_frame, "Зниження смертності карантином (%):")
        self.quarantine_mortality_reduction_entry = self.create_entry(settings_frame, "30")
        self.quarantine_mortality_reduction_entry.grid(row=22, column=1, padx=10, pady=5)

        # Використовуємо grid для кнопок
        self.create_button(self.root, "Запустити симуляцію", self.run_simulation).grid(row=23, column=0, padx=10, pady=5, sticky="nsew")
        self.create_button(self.root, "Переглянути результати", self.show_results).grid(row=24, column=0, padx=10, pady=5, sticky="nsew")
        self.create_button(self.root, "Назад", self.show_main_menu).grid(row=25, column=0, padx=10, pady=5, sticky="nsew")
    
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
        settings_frame.grid_rowconfigure(11, weight=1)
        settings_frame.grid_rowconfigure(12, weight=1)
        settings_frame.grid_rowconfigure(13, weight=1)
        settings_frame.grid_rowconfigure(14, weight=1)
        settings_frame.grid_rowconfigure(15, weight=1)
        settings_frame.grid_rowconfigure(16, weight=1)
        settings_frame.grid_rowconfigure(17, weight=1)
        settings_frame.grid_rowconfigure(18, weight=1)
        settings_frame.grid_rowconfigure(19, weight=1)
        settings_frame.grid_rowconfigure(20, weight=1)
        settings_frame.grid_rowconfigure(21, weight=1)
        settings_frame.grid_rowconfigure(22, weight=1)

        # Для стовпців теж можна налаштувати
        settings_frame.grid_columnconfigure(0, weight=1)
        settings_frame.grid_columnconfigure(1, weight=3)
    

    def run_simulation(self):
        # Отримуємо ім'я експерименту
        experiment_name = self.experiment_name_entry.get()

        # Отримуємо загальну кількість людей
        total_population = int(self.population_entry.get())

        # Отримуємо відсотки за статтю
        male_percent = float(self.male_entry.get())
        female_percent = float(self.female_entry.get())

        # Отримуємо відсотки вікових груп
        children_percentage = float(self.children_entry.get())
        young_adults_percentage = float(self.young_adults_entry.get())
        middle_age_percentage = float(self.middle_age_entry.get())
        senior_percentage = float(self.senior_entry.get())

        # Отримуємо коефіцієнти зараження та одужання
        beta = float(self.beta_entry.get())
        gamma = float(self.gamma_entry.get())

        # Отримуємо кількість днів симуляції
        days = int(self.days_entry.get())

        # Отримуємо коефіцієнти летальності для кожної вікової групи
        death_rate_children = float(self.death_rate_children_entry.get())
        death_rate_young_adults = float(self.death_rate_young_adults_entry.get())
        death_rate_middle_age = float(self.death_rate_middle_age_entry.get())
        death_rate_senior = float(self.death_rate_senior_entry.get())

        male_mortality = float(self.male_mortality_entry.get())
        female_mortality = float(self.female_mortality_entry.get())

        # Отримуємо дані щодо вакцинації та карантину
        vaccine_percent = float(self.vaccine_percent_entry.get())
        quarantine_percent = float(self.quarantine_percent_entry.get())
        vaccine_infection_reduction = float(self.vaccine_infection_reduction_entry.get())
        vaccine_mortality_reduction = float(self.vaccine_mortality_reduction_entry.get())
        quarantine_infection_reduction = float(self.quarantine_infection_reduction_entry.get())
        quarantine_mortality_reduction = float(self.quarantine_mortality_reduction_entry.get())

       
        from model import Population
        population = Population(
            total_population,
            children_percentage, young_adults_percentage, middle_age_percentage, senior_percentage,
            death_rate_children, death_rate_young_adults, death_rate_middle_age, death_rate_senior,
            male_percent, female_percent, male_mortality, female_mortality
        )
    
        data = parallel_simulation(
            population, beta, gamma, days, 4,
            vaccine_percent, vaccine_infection_reduction, vaccine_mortality_reduction,
            quarantine_percent, quarantine_infection_reduction, quarantine_mortality_reduction
        )
    
        messagebox.showinfo(
            "Симуляція завершена",
            f"Експеримент: {experiment_name}\nСимуляцію завершено. Перегляньте результати"
        )
    
        from visualisation import (
            plot_results,
            plot_age_mortality,
            plot_vaccine_quarantine_effects,
            plot_gender_mortality,
            plot_cumulative_infected,
            plot_peak_infected,
            plot_gender_distribution,
            plot_age_gender_mortality
        )
    
        plot_results(
            data['susceptible'],
            data['infected'],
            data['recovered'],
            data['dead']
        )
        plot_age_mortality(data['age_deaths'])
        plot_vaccine_quarantine_effects(*data['vaccine_quarantine_effects'])
        plot_gender_mortality(*data['gender_deaths'])
        plot_cumulative_infected(data['cumulative_infected'], days)
        plot_peak_infected(data['infected'], data['peak'][1])
    
        # Нові графіки, які раніше вимагали додаткових обчислень
        plot_gender_distribution(*data['population_gender'])
        plot_age_gender_mortality(data['age_gender_deaths'])

   
    def show_results(self):
        if not os.path.exists(TEMP_GRAPH_PATH):
            messagebox.showerror("Помилка", "Немає збережених результатів!")
            returnн


        # Отримуємо результат симуляції
        population_obj = self.get_population_input()  # Отримуємо об'єкт популяції (populatio_obj)

        vaccination_value = float(self.vaccine_percent_entry.get()) 
        quarantine_value = float(self.quarantine_percent_entry.get())

        # Отримуємо зниження інфікування та смертності через вакцинацію та карантин
        vaccine_infection_reduction = float(self.vaccine_infection_reduction_entry.get()) / 100
        vaccine_mortality_reduction = float(self.vaccine_mortality_reduction_entry.get()) / 100
        quarantine_infection_reduction = float(self.quarantine_infection_reduction_entry.get()) / 100
        quarantine_mortality_reduction = float(self.quarantine_mortality_reduction_entry.get()) / 100


        results = parallel_simulation(
            population_obj,
            beta=float(self.beta_entry.get()),
            gamma=float(self.gamma_entry.get()),
            days=int(self.days_entry.get()),
            children_percent=float(self.children_entry.get()),
            young_adults_percent=float(self.young_adults_entry.get()),
            middle_age_percent=float(self.middle_age_entry.get()),
            senior_percent=float(self.senior_entry.get()),
            death_rate_children=float(self.death_rate_children_entry.get()),
            death_rate_young_adults=float(self.death_rate_young_adults_entry.get()),
            death_rate_middle_age=float(self.death_rate_middle_age_entry.get()),
            death_rate_senior=float(self.death_rate_senior_entry.get()),
            vaccination=float(self.vaccine_percent_entry.get()),
            quarantine=float(self.quarantine_percent_entry.get()), 
            vaccine_infection_reduction=vaccine_infection_reduction,
            vaccine_mortality_reduction=vaccine_mortality_reduction,
            quarantine_infection_reduction=quarantine_infection_reduction,
            quarantine_mortality_reduction=quarantine_mortality_reduction,
            num_processes=8
        )

        # Отримуємо всі значення з результатів
        final_susceptible, final_infected, final_recovered, final_deaths, total_mortality, children_mortality, \
        young_adults_mortality, middle_age_mortality, senior_mortality, vaccination_impact, vaccination_mortality_impact, \
        quarantine_impact, quarantine_mortality_impact = results

        # Проводимо візуалізацію результатів
        plot_results(final_susceptible, final_infected, final_recovered, final_deaths, save_path=TEMP_GRAPH_PATH)

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
        img_label.grid(row=1, column=0, padx=10, pady=10)

        # Формуємо текстові результати
        text_result = f"Experiment: {self.experiment_name_entry.get()}\n"
        text_result += f"Population: {self.population_entry.get()}, β: {self.beta_entry.get()}, γ: {self.gamma_entry.get()}, Days: {self.days_entry.get()}\n"
        text_result += f"Max infected: {int(self.max_infected)} on day {self.max_infected_day}\n"
        text_result += f"Total infected during the period: {int(self.total_infected)}\n"

        # Мортальність
        text_result += f"Total mortality: {round(total_mortality):.0f} people ({round(total_mortality * 100 / float(self.population_entry.get())):.2f}%)\n"
        text_result += f"Children mortality: {round(children_mortality):.0f} people ({round(children_mortality * 100 / population_obj.children):.2f}%)\n"
        text_result += f"Younger adults mortality: {round(young_adults_mortality):.0f} people ({round(young_adults_mortality * 100 / population_obj.young_adults):.2f}%)\n"
        text_result += f"Middle-aged mortality: {round(middle_age_mortality):.0f} people ({round(middle_age_mortality * 100 / population_obj.middle_aged):.2f}%)\n"
        text_result += f"Seniors mortality: {round(senior_mortality):.0f} people ({round(senior_mortality * 100 / population_obj.senior):.2f}%)\n"

        # Вплив вакцинації та карантину
        text_result += f"Vaccination rate: {round(vaccination_value * 100, 2):.2f}%\n"
        text_result += f"Impact of vaccination on infection: {round(vaccination_impact, 2):.2f}% reduction\n"
        text_result += f"Impact of vaccination on mortality: {round(vaccination_mortality_impact, 2):.2f}% reduction\n"

        text_result += f"Quarantine measures applied: {round(quarantine_value * 100, 2):.2f}%\n"
        text_result += f"Impact of quarantine on infection: {round(quarantine_impact, 2):.2f}% reduction\n"
        text_result += f"Impact of quarantine on mortality: {round(quarantine_mortality_impact, 2):.2f}% reduction\n"


        # Розміщення тексту результату
        result_text_label = tk.Label(result_window, text=text_result, font=("Arial", 12), bg="#f4f4f4", justify="left")
        result_text_label.grid(row=2, column=0, padx=10, pady=10)

        # Розміщення кнопки для збереження результатів
        save_button = self.create_button(result_window, "Зберегти в PDF", lambda: self.save_results(result_window))
        save_button.grid(row=3, column=0, pady=10)


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