import numpy as np
import matplotlib.pyplot as plt
import os

# Переконуємось, що папка temp існує
os.makedirs("temp", exist_ok=True)

def _save_and_close(fig_name):
    plt.savefig(os.path.join("temp", fig_name))
    plt.close()

def plot_results(susceptible, infected, recovered, dead):
    try:
        days = range(len(susceptible))
        plt.figure(figsize=(10, 6))
        plt.plot(days, susceptible, label='Сприйнятливі')
        plt.plot(days, infected, label='Заражені')
        plt.plot(days, recovered, label='Одужалі')
        plt.plot(days, dead, label='Померлі')
        plt.xlabel('Дні')
        plt.ylabel('Кількість осіб')
        plt.legend()
        plt.grid(True)
    except Exception:
        plt.figure(figsize=(10, 6))
        plt.xlabel('Дні')
        plt.ylabel('Кількість осіб')
        plt.grid(True)
    finally:
        _save_and_close("results.png")

def plot_gender_distribution(male_total, female_total):
    try:
        labels = ['Чоловіки', 'Жінки']
        sizes = [male_total, female_total]
        total = male_total + female_total
        def autopct_format(pct):
            val = int(np.round(pct * total / 100.0))
            return f"{pct:.1f}%\n({val})"

        plt.figure(figsize=(6,6))
        plt.pie(sizes, labels=labels, autopct=autopct_format, startangle=90)
        plt.axis('equal')
    except Exception:
        plt.figure(figsize=(6,6))
        plt.xlabel('')
        plt.ylabel('')
    finally:
        _save_and_close("population_gender_distribution.png")

def plot_gender_mortality(male_dead, female_dead):
    try:
        labels = ['Чоловіки', 'Жінки']
        sizes = [male_dead, female_dead]
        total = male_dead + female_dead
        if total == 0:
            raise ValueError("No mortality data")
        def autopct_format(pct):
            val = int(np.round(pct * total / 100.0))
            return f"{pct:.1f}%\n({val})"

        plt.figure(figsize=(6,6))
        plt.pie(sizes, labels=labels, autopct=autopct_format, startangle=90)
        plt.axis('equal')
    except Exception:
        plt.figure(figsize=(6,6))
    finally:
        _save_and_close("gender_mortality.png")

def plot_age_mortality(age_deaths):
    try:
        days = range(len(next(iter(age_deaths.values()))))
        plt.figure(figsize=(10, 6))
        for group, death_series in age_deaths.items():
            plt.plot(days, death_series, label=f'Група: {group}')
        plt.xlabel('Дні')
        plt.ylabel('Кількість померлих')
        plt.legend()
        plt.grid(True)
    except Exception:
        plt.figure(figsize=(10, 6))
        plt.xlabel('Дні')
        plt.ylabel('Кількість померлих')
        plt.grid(True)
    finally:
        _save_and_close("age_mortality.png")

def plot_age_gender_mortality(age_gender_deaths):
    try:
        groups = list(age_gender_deaths.keys())
        male = [age_gender_deaths[g][0] for g in groups]
        female = [age_gender_deaths[g][1] for g in groups]
        x = np.arange(len(groups))
        width = 0.35

        plt.figure(figsize=(10, 6))
        plt.bar(x - width/2, male, width, label='Чоловіки')
        plt.bar(x + width/2, female, width, label='Жінки')
        plt.xlabel('Вікові групи')
        plt.ylabel('Кількість померлих')
        plt.xticks(x, groups, rotation=15, ha='right')
        plt.legend()
        plt.grid(True, axis='y')
    except Exception:
        plt.figure(figsize=(10, 6))
        plt.xlabel('Вікові групи')
        plt.ylabel('Кількість померлих')
        plt.grid(True, axis='y')
    finally:
        _save_and_close("age_gender_mortality.png")

def plot_vaccine_quarantine_effects(vacc_inf_eff, vacc_mort_eff, quar_inf_eff, quar_mort_eff):
    try:
        labels = ['Інфікування', 'Смертність']
        vaccine_effects = [vacc_inf_eff, vacc_mort_eff]
        quarantine_effects = [quar_inf_eff, quar_mort_eff]
        x = np.arange(len(labels))
        width = 0.35

        plt.figure(figsize=(8, 6))
        plt.bar(x - width/2, vaccine_effects, width, label='Вакцинація')
        plt.bar(x + width/2, quarantine_effects, width, label='Карантин')
        plt.xlabel('Показники ефекту')
        plt.ylabel('Відсоток зменшення')
        plt.xticks(x, labels)
        plt.legend()
        plt.grid(True, axis='y')
    except Exception:
        plt.figure(figsize=(8, 6))
        plt.xlabel('Показники ефекту')
        plt.ylabel('Відсоток зменшення')
        plt.grid(True, axis='y')
    finally:
        _save_and_close("vaccine_quarantine_effects.png")

def plot_cumulative_infected(cumulative_infected, days):
    try:
        x = range(days)
        plt.figure(figsize=(10, 6))
        plt.plot(x, cumulative_infected, marker='o', linestyle='-')
        plt.xlabel('Дні')
        plt.ylabel('Кількість інфікованих (кумулятивно)')
        plt.grid(True)
    except Exception:
        plt.figure(figsize=(10, 6))
        plt.xlabel('Дні')
        plt.ylabel('Кількість інфікованих (кумулятивно)')
        plt.grid(True)
    finally:
        _save_and_close("cumulative_infected.png")

def plot_peak_infected(infected, peak_day):
    try:
        days = range(len(infected))
        plt.figure(figsize=(10, 6))
        plt.plot(days, infected, label='Заражені')
        plt.axvline(x=peak_day, linestyle='--', label=f'Пік інфекції (День {peak_day})')
        plt.xlabel('Дні')
        plt.ylabel('Кількість заражених')
        plt.legend()
        plt.grid(True)
    except Exception:
        plt.figure(figsize=(10, 6))
        plt.xlabel('Дні')
        plt.ylabel('Кількість заражених')
        plt.grid(True)
    finally:
        _save_and_close("peak_infected.png")

def plot_infection_durations(durations: dict):
    try:
        groups = list(durations.keys())
        T = [durations[g] for g in groups]
        plt.figure(figsize=(10, 6))
        plt.bar(groups, T)
        plt.ylabel("Середня тривалість інфекції, дні")
        plt.xlabel("Вікова група")
        plt.xticks(rotation=15, ha='right')
        plt.tight_layout()
    except Exception:
        plt.figure(figsize=(10, 6))
        plt.ylabel("Середня тривалість інфекції, дні")
        plt.xlabel("Вікова група")
        plt.tight_layout()
    finally:
        _save_and_close("infection_durations.png")
