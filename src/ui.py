# ui.py
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, Label, Button
import re
import os
from simulation import parallel_simulation
from visualisation import plot_results
from save_results import save_results_to_pdf
import numpy as np
from model import Population
from save_results import save_results_to_pdf
import shutil

RESULTS_DIR = "data"
TEMP_GRAPH_PATH = os.path.join(RESULTS_DIR, "temp_graph.png")

class SimulationApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Симуляція поширення вірусу")
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
    
    def show_main_menu(self):
        # Очищаємо всі віджети
        for widget in self.root.winfo_children():
            widget.destroy()

        # Встановлюємо розмір і центруємо
        self.root.geometry("400x300")
        self.center_window(self.root, 400, 300)

        # Контейнер для всіх елементів
        main_frame = tk.Frame(self.root, bg="#f4f4f4")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)

        # Заголовок
        lbl = tk.Label(
            main_frame,
            text="Оберіть опцію:",
            font=("Arial", 14),
            bg="#f4f4f4"
        )
        lbl.grid(row=0, column=0, sticky="we", pady=(0, 20))

        # Кнопки
        btn1 = tk.Button(
            main_frame,
            text="Створити новий тест",
            command=self.show_simulation_settings,
            font=("Arial", 12)
        )
        btn1.grid(row=1, column=0, sticky="we", pady=10)

        btn2 = tk.Button(
            main_frame,
            text="Обрахувати параметри",
            command=self.show_calculate_parameters_settings,
            font=("Arial", 12)
        )
        btn2.grid(row=2, column=0, sticky="we", pady=10)

        btn3 = tk.Button(
            main_frame,
            text="Обрахувати коефіціенти",
            command=self.show_calculate_factors_settings,
            font=("Arial", 12)
        )
        btn3.grid(row=3, column=0, sticky="we", pady=10)

        btn4 = tk.Button(
            main_frame,
            text="Завантажити параметри",
            command=self.load_parameters,
            font=("Arial", 12)
        )
        btn4.grid(row=4, column=0, sticky="we", pady=10)

    def show_simulation_settings(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("800x700")
        self.center_window(self.root, 800, 700)

        outer_frame = tk.Frame(self.root, bg="#f4f4f4")
        outer_frame.pack(fill="both", expand=True, padx=10, pady=20)

        settings_frame = tk.Frame(outer_frame, bg="#f4f4f4")
        settings_frame.pack(fill="both", expand=True)

        for col in range(3):
            settings_frame.grid_columnconfigure(col, weight=1, uniform="col")

        fields = [
            ("Назва експерименту",                "experiment_name_entry",                  "Test_Infection_X"),
            ("Популяція",                         "population_entry",                       "1000"),
            ("% чоловіків",                       "male_entry",                             "60"),
            ("% жінок",                           "female_entry",                           "40"),
            ("% дітей (0–14 років)",              "children_entry",                         "25"),
            ("% молодь (15–34 років)",            "young_adults_entry",                     "25"),
            ("% середній вік (35–64)",            "middle_age_entry",                       "25"),
            ("% похилі (65+)",                    "senior_entry",                           "25"),
            ("Коеф. зараження (β)",               "beta_entry",                             "0.4"),
            ("Коеф. одужання (γ)",                "gamma_entry",                            "0.1"),
            ("Кількість днів",                    "days_entry",                             "100"),
            ("Летальність дітей (%)",             "death_rate_children_entry",              "7"),
            ("Летальність молодих (%)",           "death_rate_young_adults_entry",          "4"),
            ("Летальність середнього віку (%)",   "death_rate_middle_age_entry",            "6"),
            ("Летальність похилого віку (%)",     "death_rate_senior_entry",                "10"),
            ("Смертність чоловіків (%)",          "male_mortality_entry",                   "70"),
            ("Смертність жінок (%)",              "female_mortality_entry",                 "30"),
            ("Вакцинація (%)",                    "vaccine_percent_entry",                  "10"),
            ("Карантин (%)",                      "quarantine_percent_entry",               "10"),
            ("↓ інфікування вакциною (%)",        "vaccine_infection_reduction_entry",      "40"),
            ("↓ смертність вакциною (%)",         "vaccine_mortality_reduction_entry",      "30"),
            ("↓ інфікування карантином (%)",      "quarantine_infection_reduction_entry",   "50"),
            ("↓ смертність карантином (%)",       "quarantine_mortality_reduction_entry",   "40"),
        ]

        for idx, (text, attr, default) in enumerate(fields):
            col = idx % 3
            row = (idx // 3) * 2

            if col == 0:
                padx = (10, 5)
            elif col == 1:
                padx = (10, 10)
            else:
                padx = (5, 10)

            lbl = tk.Label(settings_frame, text=text, font=("Arial", 10), bg="#f4f4f4")
            lbl.grid(row=row, column=col, padx=padx, pady=(10, 0), sticky="w")

            entry = tk.Entry(settings_frame, font=("Arial", 10), bd=2, relief="solid")
            entry.insert(0, default)
            entry.grid(row=row+1, column=col, padx=padx, pady=(0, 10), sticky="we")

            setattr(self, attr, entry)

        buttons_frame = tk.Frame(outer_frame, bg="#f4f4f4")
        buttons_frame.pack(fill="x", pady=10)

        for col in range(3):
            buttons_frame.grid_columnconfigure(col, weight=1, uniform="btn")

        btn_run  = tk.Button(buttons_frame, text="Запустити симуляцію",    command=self.run_simulation,    height=2)
        btn_view = tk.Button(buttons_frame, text="Зберегти результати та параметри", command=self.save_results,      height=2)
        btn_back = tk.Button(buttons_frame, text="Назад",                  command=self.show_main_menu,    height=2)

        btn_run .grid(row=0, column=0, padx=(10, 5), pady=5, sticky="we")
        btn_view.grid(row=0, column=1, padx=(10, 10), pady=5, sticky="we")
        btn_back.grid(row=0, column=2, padx=(5, 10), pady=5, sticky="we")

    def run_simulation(self):
        if not self.validate_parameters():
            return

        experiment_name = self.experiment_name_entry.get()

        total_population = int(self.population_entry.get())

        male_percent = float(self.male_entry.get())
        female_percent = float(self.female_entry.get())

        children_percentage = float(self.children_entry.get())
        young_adults_percentage = float(self.young_adults_entry.get())
        middle_age_percentage = float(self.middle_age_entry.get())
        senior_percentage = float(self.senior_entry.get())

        beta = float(self.beta_entry.get())
        gamma = float(self.gamma_entry.get())

        days = int(self.days_entry.get())

        death_rate_children = float(self.death_rate_children_entry.get())
        death_rate_young_adults = float(self.death_rate_young_adults_entry.get())
        death_rate_middle_age = float(self.death_rate_middle_age_entry.get())
        death_rate_senior = float(self.death_rate_senior_entry.get())

        male_mortality = float(self.male_mortality_entry.get())
        female_mortality = float(self.female_mortality_entry.get())

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
            plot_age_gender_mortality,
            plot_infection_durations
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
        plot_gender_distribution(*data['population_gender'])
        plot_age_gender_mortality(data['age_gender_deaths'])
        plot_infection_durations(data['infection_durations'])

    def save_parameters_to_txt(self):
        parameters_txt_path = os.path.join(RESULTS_DIR, "simulation_parameters.txt")

        with open(parameters_txt_path, "w", encoding="utf-8") as f:
         f.write(f"Назва експерименту: {self.experiment_name_entry.get()}\n")
         f.write(f"Популяція: {self.population_entry.get()}\n")
         f.write(f"% чоловіків: {self.male_entry.get()}\n")
         f.write(f"% жінок: {self.female_entry.get()}\n")
         f.write(f"% дітей (0–14 років): {self.children_entry.get()}\n")
         f.write(f"% молодь (15–34 років): {self.young_adults_entry.get()}\n")
         f.write(f"% середній вік (35–64): {self.middle_age_entry.get()}\n")
         f.write(f"% похилі (65+): {self.senior_entry.get()}\n")
         f.write(f"Коеф. зараження (β): {self.beta_entry.get()}\n")
         f.write(f"Коеф. одужання (γ): {self.gamma_entry.get()}\n")
         f.write(f"Кількість днів: {self.days_entry.get()}\n")
         f.write(f"Летальність дітей (%): {self.death_rate_children_entry.get()}\n")
         f.write(f"Летальність молодих (%): {self.death_rate_young_adults_entry.get()}\n")
         f.write(f"Летальність середнього віку (%): {self.death_rate_middle_age_entry.get()}\n")
         f.write(f"Летальність похилого віку (%): {self.death_rate_senior_entry.get()}\n")
         f.write(f"Смертність чоловіків (%): {self.male_mortality_entry.get()}\n")
         f.write(f"Смертність жінок (%): {self.female_mortality_entry.get()}\n")
         f.write(f"Вакцинація (%): {self.vaccine_percent_entry.get()}\n")
         f.write(f"Карантин (%): {self.quarantine_percent_entry.get()}\n")
         f.write(f"↓ інфікування вакциною (%): {self.vaccine_infection_reduction_entry.get()}\n")
         f.write(f"↓ смертність вакциною (%): {self.vaccine_mortality_reduction_entry.get()}\n")
         f.write(f"↓ інфікування карантином (%): {self.quarantine_infection_reduction_entry.get()}\n")
         f.write(f"↓ смертність карантином (%): {self.quarantine_mortality_reduction_entry.get()}\n")

    def save_results(self):
        self.save_parameters_to_txt()
        pdf_path = save_results_to_pdf()
        messagebox.showinfo("Збережено", f"Результати збережено в data/")

    def show_calculate_parameters_settings(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("800x700")
        self.center_window(self.root, 800, 700)

        outer_frame = tk.Frame(self.root, bg="#f4f4f4")
        outer_frame.pack(fill="both", expand=True, padx=10, pady=20)

        settings_frame = tk.Frame(outer_frame, bg="#f4f4f4")
        settings_frame.pack(fill="both", expand=True)

        for col in range(3):
            settings_frame.grid_columnconfigure(col, weight=1, uniform="col")

        fields = [
            ("Кількість людей",                      "population_entry",             "1000"),
            
            ("Кількість чоловіків",                  "male_population_entry",        "700"),
            ("Кількість жінок",                      "female_population_entry",      "300"),

            ("Кількість дітей (0–14 років)",         "children_population_entry",    "250"),
            ("Кількість молодь (15–34 років)",       "youth_population_entry",       "250"),
            ("Кількість середній вік (35–64)",       "middle_population_entry",      "250"),
            ("Кількість похилі (65+)",               "senior_population_entry",      "250"),
           
            ("Захворіло чоловіків",                  "infected_male_entry",          "350"),
            ("Захворіло жінок",                      "infected_female_entry",        "150"),

            ("Захворіло дітей (0–14)",               "infected_children_entry",      "100"),
            ("Захворіло молодь (15–34)",             "infected_youth_entry",         "150"),
            ("Захворіло середній вік (35–64)",       "infected_middle_entry",        "150"),
            ("Захворіло похилі (65+)",               "infected_senior_entry",        "100"),

            ("Померло чоловіків",                 "male_death_entry",             "30"),
            ("Померло жінок",                     "female_death_entry",           "20"),

            ("Померло дітей (0–14)",              "death_children_entry",         "15"),
            ("Померло молодь (15–34)",            "death_youth_entry",            "10"),
            ("Померло середній вік (35–64)",      "death_middle_entry",           "10"),
            ("Померло похилі (65+)",              "death_senior_entry",           "15"),
        ]

        for idx, (text, attr, default) in enumerate(fields):
            col = idx % 3
            row = (idx // 3) * 2
            if col == 0:
                padx = (10, 5)
            elif col == 1:
                padx = (10, 10)
            else:
                padx = (5, 10)
            lbl = tk.Label(settings_frame, text=text, font=("Arial", 10), bg="#f4f4f4")
            lbl.grid(row=row, column=col, padx=padx, pady=(10, 0), sticky="w")
            entry = tk.Entry(settings_frame, font=("Arial", 10), bd=2, relief="solid")
            entry.insert(0, default)
            entry.grid(row=row+1, column=col, padx=padx, pady=(0, 10), sticky="we")
            setattr(self, attr, entry)

        buttons_frame = tk.Frame(outer_frame, bg="#f4f4f4")
        buttons_frame.pack(fill="x", pady=10)
        for col in range(3):
            buttons_frame.grid_columnconfigure(col, weight=1, uniform="btn")
        btn_calc = tk.Button(buttons_frame, text="Обрахувати параметри", command=self.calculate_parameters, height=2)
        btn_save = tk.Button(buttons_frame, text="Зберегти параметри", command=self.save_calculation_parameters, height=2)
        btn_back = tk.Button(buttons_frame, text="Назад", command=self.show_main_menu, height=2)
        btn_calc.grid(row=0, column=0, padx=(10, 5), pady=5, sticky="we")
        btn_save.grid(row=0, column=1, padx=(5, 5), pady=5, sticky="we")
        btn_back.grid(row=0, column=2, padx=(5, 10), pady=5, sticky="we")
        
    def save_calculation_parameters(self):
        source_file = os.path.join("temp", "calculate_parameters.txt")
        destination_file = os.path.join("data", "calculate_parameters.txt")

        try:
            if os.path.exists(source_file):
                shutil.copy(source_file, destination_file)

                messagebox.showinfo("Успіх", "Файл успішно збережно в 'data/calculate_parameters.txt.txt'")
            else:
                messagebox.showerror("Помилка", f"Файл не знайдений: {source_file}")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося зберегти файл: {e}")

    def calculate_parameters(self):
        if not self.validate_parameters_for_calculate():
            return

        try:
            population = float(self.population_entry.get())
            male = float(self.male_population_entry.get())
            female = float(self.female_population_entry.get())

            children = float(self.children_population_entry.get())
            youth = float(self.youth_population_entry.get())
            middle = float(self.middle_population_entry.get())
            senior = float(self.senior_population_entry.get())

            infected_children = float(self.infected_children_entry.get())
            infected_youth = float(self.infected_youth_entry.get())
            infected_middle = float(self.infected_middle_entry.get())
            infected_senior = float(self.infected_senior_entry.get())

            death_children = float(self.death_children_entry.get())
            death_youth = float(self.death_youth_entry.get())
            death_middle = float(self.death_middle_entry.get())
            death_senior = float(self.death_senior_entry.get())

            infected_male = float(self.infected_male_entry.get())
            infected_female = float(self.infected_female_entry.get())
            death_male = float(self.male_death_entry.get())
            death_female = float(self.female_death_entry.get())

            male_percent = round((male / population) * 100, 2)
            female_percent = round((female / population) * 100, 2)

            children_percent = round((children / population) * 100, 2)
            youth_percent = round((youth / population) * 100, 2)
            middle_percent = round((middle / population) * 100, 2)
            senior_percent = round((senior / population) * 100, 2)

            death_rate_children = round((death_children / infected_children) * 100, 2) if infected_children > 0 else 0
            death_rate_youth = round((death_youth / infected_youth) * 100, 2) if infected_youth > 0 else 0
            death_rate_middle = round((death_middle / infected_middle) * 100, 2) if infected_middle > 0 else 0
            death_rate_senior = round((death_senior / infected_senior) * 100, 2) if infected_senior > 0 else 0

            total_deaths = death_children + death_youth + death_middle + death_senior
            male_mortality = round((death_male / total_deaths) * 100, 2) if total_deaths > 0 else 0
            female_mortality = round((death_female / total_deaths) * 100, 2) if total_deaths > 0 else 0

            output_file = "temp/calculate_parameters.txt"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(f"Популяція: {population}\n")
                f.write(f"% чоловіків: {male_percent}%\n")
                f.write(f"% жінок: {female_percent}%\n")
                f.write(f"% дітей (0–14 років): {children_percent}%\n")
                f.write(f"% молодь (15–34 років): {youth_percent}%\n")
                f.write(f"% середній вік (35–64): {middle_percent}%\n")
                f.write(f"% похилі (65+): {senior_percent}%\n")
                f.write(f"Летальність дітей (%): {death_rate_children}%\n")
                f.write(f"Летальність молодих (%): {death_rate_youth}%\n")
                f.write(f"Летальність середнього віку (%): {death_rate_middle}%\n")
                f.write(f"Летальність похилого віку (%): {death_rate_senior}%\n")
                f.write(f"Смертність чоловіків (%): {male_mortality}%\n")
                f.write(f"Смертність жінок (%): {female_mortality}%\n")

            messagebox.showinfo("Успіх", f"Параметри успішно обчислено")

        except Exception as e:
            messagebox.showerror("Помилка", f"Помилка при обчисленні параметрів:\n{e}")

    def show_calculate_factors_settings(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("800x700")
        self.center_window(self.root, 800, 700)

        outer_frame = tk.Frame(self.root, bg="#f4f4f4")
        outer_frame.pack(fill="both", expand=True, padx=10, pady=20)

        settings_frame = tk.Frame(outer_frame, bg="#f4f4f4")
        settings_frame.pack(fill="both", expand=True)

        for col in range(3):
            settings_frame.grid_columnconfigure(col, weight=1, uniform="col")

        fields = [
            ("Кількість контактів на день", "entry_contacts", "10"),
            ("Ймовірність зараження при контакті 0–1", "entry_infection_prob", "0.2"),
            ("Середня тривалість хвороби (днів)", "entry_disease_duration", "10")
        ]

        for idx, (text, attr, default) in enumerate(fields):
            col = idx % 3
            row = (idx // 3) * 2
            padx = (10, 5) if col == 0 else (10, 10) if col == 1 else (5, 10)

            lbl = tk.Label(settings_frame, text=text, font=("Arial", 10), bg="#f4f4f4")
            lbl.grid(row=row, column=col, padx=padx, pady=(10, 0), sticky="w")
            entry = tk.Entry(settings_frame, font=("Arial", 10), bd=2, relief="solid")
            entry.insert(0, default)
            entry.grid(row=row+1, column=col, padx=padx, pady=(0, 10), sticky="we")
            setattr(self, attr, entry)

        buttons_frame = tk.Frame(outer_frame, bg="#f4f4f4")
        buttons_frame.pack(fill="x", pady=10)
        for col in range(3):
            buttons_frame.grid_columnconfigure(col, weight=1, uniform="btn")

        btn_calc = tk.Button(buttons_frame, text="Обрахувати коефіцієнти", command=self.calculate_factors, height=2)
        btn_save = tk.Button(buttons_frame, text="Зберегти коефіцієнти", command=self.save_calculation_factors, height=2)
        btn_back = tk.Button(buttons_frame, text="Назад", command=self.show_main_menu, height=2)
        btn_calc.grid(row=0, column=0, padx=(10, 5), pady=5, sticky="we")
        btn_save.grid(row=0, column=1, padx=(5, 5), pady=5, sticky="we")
        btn_back.grid(row=0, column=2, padx=(5, 10), pady=5, sticky="we")

    def save_calculation_factors(self):
        source_file = os.path.join("temp", "calculate_factors.txt")
        destination_file = os.path.join("data", "calculate_factors.txt")

        try:
            if os.path.exists(source_file):
                shutil.copy(source_file, destination_file)

                messagebox.showinfo("Успіх", "Файл успішно збережно в 'data/calculate_factors.txt'")
            else:
                messagebox.showerror("Помилка", f"Файл не знайдений: {source_file}")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося зберегти файл: {e}")

    def calculate_factors(self):
        if not self.validate_factors():
            return

        try:
            contacts_per_day = float(self.entry_contacts.get())
            infection_prob = float(self.entry_infection_prob.get())
            duration = float(self.entry_disease_duration.get())

            beta = contacts_per_day * infection_prob * 0.1
            gamma = 1 / duration

            output_file = "temp/calculate_factors.txt"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(f"Коефіцієнт зараження (β): {beta:.2f}\n")
                f.write(f"Коефіцієнт одужання (γ): {gamma:.2f}\n")

            messagebox.showinfo("Успіх", f"Коефіцієнти успішно обчислені:\n")

        except Exception as e:
            messagebox.showerror("Помилка", f"Помилка при обчисленні коефіцієнтів:\n{e}")

    def load_parameters(self):
        file_path = filedialog.askopenfilename(
            title="Виберіть файл з параметрами",
            filetypes=[("Text files", "*.txt")]
        )

        if file_path:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                def extract_number(line):
                    match = re.search(r"\d+(\.\d+)?", line)
                    return match.group(0) if match else None

                self.show_simulation_settings()

                self.experiment_name_entry.delete(0, tk.END)
                self.experiment_name_entry.insert(0, lines[0].strip())

                self.population_entry.delete(0, tk.END)
                self.population_entry.insert(0, extract_number(lines[1])) 

                self.male_entry.delete(0, tk.END)
                self.male_entry.insert(0, extract_number(lines[2]))

                self.female_entry.delete(0, tk.END)
                self.female_entry.insert(0, extract_number(lines[3]))

                self.children_entry.delete(0, tk.END)
                self.children_entry.insert(0, extract_number(lines[4]))

                self.young_adults_entry.delete(0, tk.END)
                self.young_adults_entry.insert(0, extract_number(lines[5]))

                self.middle_age_entry.delete(0, tk.END)
                self.middle_age_entry.insert(0, extract_number(lines[6]))

                self.senior_entry.delete(0, tk.END)
                self.senior_entry.insert(0, extract_number(lines[7]))

                self.beta_entry.delete(0, tk.END)
                self.beta_entry.insert(0, extract_number(lines[8]))

                self.gamma_entry.delete(0, tk.END)
                self.gamma_entry.insert(0, extract_number(lines[9]))

                self.days_entry.delete(0, tk.END)
                self.days_entry.insert(0, extract_number(lines[10]))

                self.death_rate_children_entry.delete(0, tk.END)
                self.death_rate_children_entry.insert(0, extract_number(lines[11]))

                self.death_rate_young_adults_entry.delete(0, tk.END)
                self.death_rate_young_adults_entry.insert(0, extract_number(lines[12]))

                self.death_rate_middle_age_entry.delete(0, tk.END)
                self.death_rate_middle_age_entry.insert(0, extract_number(lines[13]))

                self.death_rate_senior_entry.delete(0, tk.END)
                self.death_rate_senior_entry.insert(0, extract_number(lines[14]))

                self.male_mortality_entry.delete(0, tk.END)
                self.male_mortality_entry.insert(0, extract_number(lines[15]))

                self.female_mortality_entry.delete(0, tk.END)
                self.female_mortality_entry.insert(0, extract_number(lines[16]))

                self.vaccine_percent_entry.delete(0, tk.END)
                self.vaccine_percent_entry.insert(0, extract_number(lines[17]))

                self.quarantine_percent_entry.delete(0, tk.END)
                self.quarantine_percent_entry.insert(0, extract_number(lines[18]))

                self.vaccine_infection_reduction_entry.delete(0, tk.END)
                self.vaccine_infection_reduction_entry.insert(0, extract_number(lines[19]))

                self.vaccine_mortality_reduction_entry.delete(0, tk.END)
                self.vaccine_mortality_reduction_entry.insert(0, extract_number(lines[20]))

                self.quarantine_infection_reduction_entry.delete(0, tk.END)
                self.quarantine_infection_reduction_entry.insert(0, extract_number(lines[21]))

                self.quarantine_mortality_reduction_entry.delete(0, tk.END)
                self.quarantine_mortality_reduction_entry.insert(0, extract_number(lines[22]))

                messagebox.showinfo("Завантажено", "Параметри симуляції успішно завантажені")
            else:
                messagebox.showerror("Помилка", "Файл з параметрами не знайдено або він не коректний!")

    def validate_parameters(self):
        male_percent = self.male_entry.get()
        female_percent = self.female_entry.get()
        children_percent = self.children_entry.get()
        young_adults_percent = self.young_adults_entry.get()
        middle_age_percent = self.middle_age_entry.get()
        senior_percent = self.senior_entry.get()

        try:
            male_percent = float(male_percent)
            female_percent = float(female_percent)
            if male_percent + female_percent != 100:
                raise ValueError("Сума % чоловіків і жінок має бути 100.")
        except ValueError as e:
            messagebox.showerror("Помилка", f"Невірні дані для % чоловіків/жінок: {str(e)}")
            return False

        try:
            children_percent = float(children_percent)
            young_adults_percent = float(young_adults_percent)
            middle_age_percent = float(middle_age_percent)
            senior_percent = float(senior_percent)
            if children_percent + young_adults_percent + middle_age_percent + senior_percent != 100:
                raise ValueError("Сума % вікових груп має бути 100.")
        except ValueError as e:
            messagebox.showerror("Помилка", f"Невірні дані для % вікових груп: {str(e)}")
            return False

        try:
            beta = float(self.beta_entry.get())
            gamma = float(self.gamma_entry.get())
            if not (0 <= beta <= 1):
                raise ValueError("Коеф. зараження (β) має бути в межах від 0 до 1.")
            if not (0 <= gamma <= 1):
                raise ValueError("Коеф. одужання (γ) має бути в межах від 0 до 1.")
        except ValueError as e:
            messagebox.showerror("Помилка", f"Невірні дані для коефіцієнтів: {str(e)}")
            return False

        try:
            death_rate_children = float(self.death_rate_children_entry.get())
            death_rate_young_adults = float(self.death_rate_young_adults_entry.get())
            death_rate_middle_age = float(self.death_rate_middle_age_entry.get())
            death_rate_senior = float(self.death_rate_senior_entry.get())
            if any(rate > 100 for rate in [death_rate_children, death_rate_young_adults, death_rate_middle_age, death_rate_senior]):
                raise ValueError("Летальність не повинна перевищувати 100%.")
        except ValueError as e:
            messagebox.showerror("Помилка", f"Невірні дані для летальності: {str(e)}")
            return False

        try:
            male_mortality = float(self.male_mortality_entry.get())
            female_mortality = float(self.female_mortality_entry.get())
            if male_mortality + female_mortality != 100:
                raise ValueError("Сума смертності чоловіків і жінок має бути 100%.")
        except ValueError as e:
            messagebox.showerror("Помилка", f"Невірні дані для смертності: {str(e)}")
            return False

        try:
            vaccine_percent = float(self.vaccine_percent_entry.get())
            quarantine_percent = float(self.quarantine_percent_entry.get())
            if any(percent > 100 for percent in [vaccine_percent, quarantine_percent]):
                raise ValueError("Вакцинація та карантин не повинні перевищувати 100%.")
        except ValueError as e:
            messagebox.showerror("Помилка", f"Невірні дані для вакцинації/карантину: {str(e)}")
            return False

        try:
            vaccine_infection_reduction = float(self.vaccine_infection_reduction_entry.get())
            vaccine_mortality_reduction = float(self.vaccine_mortality_reduction_entry.get())
            quarantine_infection_reduction = float(self.quarantine_infection_reduction_entry.get())
            quarantine_mortality_reduction = float(self.quarantine_mortality_reduction_entry.get())
            if any(percent > 100 for percent in [vaccine_infection_reduction, vaccine_mortality_reduction, 
                                                  quarantine_infection_reduction, quarantine_mortality_reduction]):
                raise ValueError("Зменшення інфікування та смертності не повинно перевищувати 100%.")
        except ValueError as e:
            messagebox.showerror("Помилка", f"Невірні дані для зменшення інфікування/смертності: {str(e)}")
            return False

        return True

    def validate_parameters_for_calculate(self):
        total_population = int(self.population_entry.get())
        male_population = int(self.male_population_entry.get())
        female_population = int(self.female_population_entry.get())

        children_population = int(self.children_population_entry.get())
        youth_population = int(self.youth_population_entry.get())
        middle_population = int(self.middle_population_entry.get())
        senior_population = int(self.senior_population_entry.get())

        infected_male = int(self.infected_male_entry.get())
        infected_female = int(self.infected_female_entry.get())

        infected_children = int(self.infected_children_entry.get())
        infected_youth = int(self.infected_youth_entry.get())
        infected_middle = int(self.infected_middle_entry.get())
        infected_senior = int(self.infected_senior_entry.get())

        male_death = int(self.male_death_entry.get())
        female_death = int(self.female_death_entry.get())

        death_children = int(self.death_children_entry.get())
        death_youth = int(self.death_youth_entry.get())
        death_middle = int(self.death_middle_entry.get())
        death_senior = int(self.death_senior_entry.get())

        if male_population + female_population != total_population:
            messagebox.showerror("Помилка", "Кількість чоловіків та жінок має дорівнювати загальній кількості людей.")
            return False

        if (children_population + youth_population + middle_population + senior_population) != total_population:
            messagebox.showerror("Помилка", "Сума кількості людей у вікових групах має дорівнювати загальній кількості людей.")
            return False

        if infected_male + infected_female > total_population:
            messagebox.showerror("Помилка", "Кількість захворілих не може перевищувати загальну кількість людей.")
            return False

        if infected_children + infected_youth + infected_middle + infected_senior > infected_male + infected_female:
            messagebox.showerror("Помилка", "Загальна кількість захворілих не може перевищувати загальну кількість людей.")
            return False

        if male_death > male_population or female_death > female_population:
            messagebox.showerror("Помилка", "Кількість померлих чоловіків чи жінок не може перевищувати кількість чоловіків чи жінок.")
            return False

        if death_children > children_population or death_youth > youth_population or death_middle > middle_population or death_senior > senior_population:
            messagebox.showerror("Помилка", "Кількість померлих у вікових групах не може перевищувати кількість людей у цих групах.")
            return False

        if death_children > infected_children or death_youth > infected_youth or death_middle > infected_middle or death_senior > infected_senior:
            messagebox.showerror("Помилка", "Кількість померлих не може перевищувати кількість захворілих в кожній віковій групі.")
            return False

        return True

    def validate_factors(self):
        try:
            contacts = float(self.entry_contacts.get())
            if contacts < 0:
                messagebox.showerror("Помилка", "Кількість контактів на день не може бути менше 0.")
                return False
    
            infection_prob = float(self.entry_infection_prob.get())
            if infection_prob < 0 or infection_prob > 1:
                messagebox.showerror("Помилка", "Ймовірність зараження при контакті повинна бути в межах 0–1.")
                return False
    
            disease_duration = float(self.entry_disease_duration.get())
            if disease_duration < 0:
                messagebox.showerror("Помилка", "Середня тривалість хвороби не може бути менше 0.")
                return False
    
            return True
    
        except ValueError:
            messagebox.showerror("Помилка", "Всі значення повинні бути числовими.")
            return False

if __name__ == "__main__":
    app = SimulationApp()
    app.run()