
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, Label, Button
import os
import shutil
from simulation import parallel_simulation
from visualisation import plot_results
from save_results import save_results_to_pdf
import numpy as np

RESULTS_DIR = "data"
TEMP_GRAPH_PATH = os.path.join(RESULTS_DIR, "temp_graph.png")

class SimulationApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Симуляція поширення вірусу")
        self.root.geometry("700x650")
        self.root.config(bg="#f4f4f4")
        self.center_window(self.root, 700, 650)  # Центруємо головне вікно
        self.results_saved = False
        self.susceptible = None
        self.infected = None
        self.recovered = None
        self.show_welcome_screen()

    def center_window(self, window, width, height):
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        window.geometry(f"{width}x{height}+{x}+{y}")

    def create_label(self, parent, text, font_size=14):
        label = tk.Label(parent, text=text, font=("Arial", font_size), bg="#f4f4f4")
        label.pack(pady=10)
        return label

    def create_button(self, parent, text, command, font_size=12):
        button = tk.Button(parent, text=text, font=("Arial", font_size), command=command, width=25, height=2, 
                           bg="#4CAF50", fg="white", relief="solid", bd=2)
        button.pack(pady=10)
        return button

    def create_entry(self, parent, default_value="", font_size=12):
        entry = tk.Entry(parent, font=("Arial", font_size), width=30, bd=2, relief="solid")
        entry.insert(0, default_value)
        entry.pack(pady=5)
        return entry

    def show_welcome_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.create_label(self.root, "Ласкаво просимо до симуляції поширення вірусу!", 16)
        self.create_button(self.root, "Почати роботу", self.show_main_menu, 14)

    def show_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.create_label(self.root, "Оберіть опцію:", 14)
        self.create_button(self.root, "Створити новий тест", self.show_simulation_settings, 12)
        self.create_button(self.root, "Завантажити параметри з файлу", self.load_parameters, 12)
        self.create_button(self.root, "Вихід", self.root.quit, 12)

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

        self.create_label(self.root, "Назва експерименту:")
        self.experiment_name_entry = self.create_entry(self.root, "Test_Infection_X")

        self.create_label(self.root, "Популяція:")
        self.population_entry = self.create_entry(self.root, "1000")

        self.create_label(self.root, "Коеф. зараження (β):")
        self.beta_entry = self.create_entry(self.root, "0.3")

        self.create_label(self.root, "Коеф. одужання (γ):")
        self.gamma_entry = self.create_entry(self.root, "0.1")

        self.create_label(self.root, "Кількість днів:")
        self.days_entry = self.create_entry(self.root, "100")

        self.create_button(self.root, "Запустити симуляцію", self.run_simulation)
        self.create_button(self.root, "Переглянути результати", self.show_results)
        self.create_button(self.root, "Назад", self.show_main_menu)

    def run_simulation(self):
        experiment_name = self.experiment_name_entry.get()
        population = int(self.population_entry.get())
        beta = float(self.beta_entry.get())
        gamma = float(self.gamma_entry.get())
        days = int(self.days_entry.get())

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
        self.center_window(result_window, 1000, 800)

        self.create_label(result_window, "Результати симуляції:", 14)

        img = tk.PhotoImage(file=TEMP_GRAPH_PATH)
        img_label = Label(result_window, image=img)
        img_label.image = img
        img_label.pack()

        text_result = f"Experiment: {self.experiment_name_entry.get()}\n"
        text_result += f"Population: {self.population_entry.get()}, β: {self.beta_entry.get()}, γ: {self.gamma_entry.get()}, Days: {self.days_entry.get()}\n"
        text_result += f"Max infected: {int(self.max_infected)} on day {self.max_infected_day}\n"
        text_result += f"Total infected during the period: {int(self.total_infected)}"

        self.create_label(result_window, text_result, 12)

        self.create_button(result_window, "Зберегти в PDF", lambda: self.save_results(result_window))


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

