import numpy as np
import matplotlib.pyplot as plt
import os

# Переконуємось, що папка temp існує
os.makedirs("temp", exist_ok=True)

def plot_results(susceptible, infected, recovered, dead):
    days = range(len(susceptible))
    plt.figure(figsize=(10, 6))
    plt.plot(days, susceptible, label='Сприйнятливі', color='blue')
    plt.plot(days, infected, label='Заражені', color='red')
    plt.plot(days, recovered, label='Одужалі', color='green')
    plt.plot(days, dead, label='Померлі', color='black')
    plt.xlabel('Дні')
    plt.ylabel('Кількість осіб')
    plt.title('Результати симуляції епідемії')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join("temp", "results.png"))
    plt.close()

def plot_gender_distribution(male_total, female_total):
    """
    Показує розподіл населення за статтю з відображенням відсотків і абсолютної кількості.
    """
    labels = ['Чоловіки', 'Жінки']
    sizes = [male_total, female_total]
    total = male_total + female_total
    
    def autopct_format(pct):
        val = int(np.round(pct * total / 100.0))
        return f"{pct:.1f}%\n({val})"

    plt.figure()
    plt.pie(sizes, labels=labels, autopct=autopct_format, startangle=90)
    plt.title('Розподіл населення за статтю')
    plt.axis('equal')
    plt.savefig(os.path.join("temp", "population_gender_distribution.png"))
    plt.close()


def plot_gender_mortality(male_dead, female_dead):
    labels = ['Чоловіки', 'Жінки']
    sizes = [male_dead, female_dead]
    total = male_dead + female_dead

    if total == 0:
        return

    def autopct_format(pct):
        val = int(np.round(pct * total / 100.0))
        return f"{pct:.1f}%\n({val})"

    plt.figure()
    plt.pie(sizes, labels=labels, autopct=autopct_format, startangle=90)
    plt.title('Розподіл смертності за статтю')
    plt.axis('equal')
    plt.savefig(os.path.join("temp", "gender_mortality.png"))
    plt.close()



def plot_age_mortality(age_deaths):
    days = range(len(next(iter(age_deaths.values()))))
    plt.figure(figsize=(10, 6))
    for group, death_series in age_deaths.items():
        plt.plot(days, death_series, label=f'Група: {group}')
    plt.xlabel('Дні')
    plt.ylabel('Кількість померлих')
    plt.title('Динаміка смертності за віковими групами')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join("temp", "age_mortality.png"))
    plt.close()

def plot_age_gender_mortality(age_gender_deaths):
    """
    Показує смертність за віковими групами з розподілом за статтю.
    age_gender_deaths: dict, ключі – назви груп, значення – кортеж (male_dead, female_dead)
    """
    groups = list(age_gender_deaths.keys())
    male = [age_gender_deaths[g][0] for g in groups]
    female = [age_gender_deaths[g][1] for g in groups]
    x = np.arange(len(groups))
    width = 0.35
    plt.figure()
    plt.bar(x - width/2, male, width, label='Чоловіки')
    plt.bar(x + width/2, female, width, label='Жінки')
    plt.xlabel('Вікові групи')
    plt.ylabel('Кількість померлих')
    plt.title('Смертність за віковими групами і статтю')
    plt.xticks(x, groups)
    plt.legend()
    plt.grid(True, axis='y')
    plt.savefig(os.path.join("temp", "age_gender_mortality.png"))
    plt.close()

def plot_vaccine_quarantine_effects(vacc_inf_eff, vacc_mort_eff, quar_inf_eff, quar_mort_eff):
    labels = ['Інфікування', 'Смертність']
    vaccine_effects = [vacc_inf_eff, vacc_mort_eff]
    quarantine_effects = [quar_inf_eff, quar_mort_eff]
    x = np.arange(len(labels))
    width = 0.35
    plt.figure(figsize=(8, 6))
    plt.bar(x - width/2, vaccine_effects, width, label='Вакцинація', color='skyblue')
    plt.bar(x + width/2, quarantine_effects, width, label='Карантин', color='lightgreen')
    plt.xlabel('Показники ефекту')
    plt.ylabel('Відсоток зменшення')
    plt.title('Порівняння ефекту вакцинації та карантину')
    plt.xticks(x, labels)
    plt.legend()
    plt.grid(True, axis='y')
    plt.savefig(os.path.join("temp", "vaccine_quarantine_effects.png"))
    plt.close()





def plot_cumulative_infected(cumulative_infected, days):
    x = range(days)
    plt.figure(figsize=(10, 6))
    plt.plot(x, cumulative_infected, marker='o', color='purple', linestyle='-')
    plt.xlabel('Дні')
    plt.ylabel('Кількість інфікованих (кумулятивно)')
    plt.title('Кумулятивна кількість інфікованих')
    plt.grid(True)
    plt.savefig(os.path.join("temp", "cumulative_infected.png"))
    plt.close()


def plot_peak_infected(infected, peak_day):
    days = range(len(infected))
    plt.figure(figsize=(10, 6))
    plt.plot(days, infected, label='Заражені', color='red')
    plt.axvline(x=peak_day, color='black', linestyle='--', label=f'Пік інфекції (День {peak_day})')
    plt.xlabel('Дні')
    plt.ylabel('Кількість заражених')
    plt.title('Графік заражених із позначенням пікового навантаження')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join("temp", "peak_infected.png"))
    plt.close()
