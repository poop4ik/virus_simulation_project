#simulation.py
from mpi4py import MPI 
import numpy as np
from model import Population
import os

def compute_group_gender_deaths(group_dead, population):
    """
    Обчислює кількість смертних за статтю для даної групи.
    Формула:
      male_weight = (male_percent / 100) * male_mort_rate
      female_weight = (female_percent / 100) * female_mort_rate
      group_male_dead = round(group_dead * (male_weight / (male_weight + female_weight)))
      group_female_dead = group_dead - group_male_dead
    """
    male_weight = (population.male_percent / 100) * population.male_mort_rate
    female_weight = (population.female_percent / 100) * population.female_mort_rate
    total_weight = male_weight + female_weight

    if total_weight == 0:
        return 0, 0

    if male_weight == 0:
        return 0, int(group_dead)

    if female_weight == 0:
        return int(group_dead), 0

    group_male_dead = int(np.round(group_dead * (male_weight / total_weight)))
    group_female_dead = group_dead - group_male_dead
    return group_male_dead, group_female_dead

def parallel_simulation(population, beta, gamma, days, num_processes,
                        vaccine_percent, vaccine_infection_reduction, vaccine_mortality_reduction,
                        quarantine_percent, quarantine_infection_reduction, quarantine_mortality_reduction):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    chunk_size = days // size
    start_day = rank * chunk_size
    end_day = (rank + 1) * chunk_size if rank != size - 1 else days

    local_results = {
        'susceptible': np.zeros(days),
        'infected': np.zeros(days),
        'recovered': np.zeros(days),
        'dead': np.zeros(days),
        'cumulative_infected': np.zeros(days)
    }

    local_age_deaths = {
        'Children': np.zeros(days),
        'Young Adults': np.zeros(days),
        'Middle Aged': np.zeros(days),
        'Senior': np.zeros(days)
    }

    max_infected = 0
    max_infected_day = 0

    for day in range(start_day, end_day):
        result = population.simulate_day(
            beta, gamma, vaccine_percent, vaccine_infection_reduction,
            vaccine_mortality_reduction, quarantine_percent,
            quarantine_infection_reduction, quarantine_mortality_reduction
        )

        for group, data in result.items():
            local_results['susceptible'][day] += data['susceptible']
            local_results['infected'][day] += data['infected']
            local_results['recovered'][day] += data['recovered']
            local_results['dead'][day] += data['dead']
            local_age_deaths[group][day] = data['dead']

        local_results['cumulative_infected'][day] = population.cumulative_infected

        if local_results['infected'][day] > max_infected:
            max_infected = local_results['infected'][day]
            max_infected_day = day

    gathered_results = comm.gather(local_results, root=0)
    gathered_age_deaths = comm.gather(local_age_deaths, root=0)
    max_infected_data = comm.gather((max_infected, max_infected_day), root=0)

    if rank == 0:
        final_susceptible = np.zeros(days)
        final_infected = np.zeros(days)
        final_recovered = np.zeros(days)
        final_dead = np.zeros(days)
        final_cumulative_infected = np.zeros(days)

        for result in gathered_results:
            final_susceptible += result['susceptible']
            final_infected += result['infected']
            final_recovered += result['recovered']
            final_dead += result['dead']
            final_cumulative_infected += result['cumulative_infected']

        final_age_deaths = {
            'Children': np.zeros(days),
            'Young Adults': np.zeros(days),
            'Middle Aged': np.zeros(days),
            'Senior': np.zeros(days)
        }
        for age_deaths in gathered_age_deaths:
            for group in final_age_deaths:
                final_age_deaths[group] += age_deaths[group]

        final_susceptible_last = int(np.round(final_susceptible[-1]))
        final_infected_last = int(np.round(final_infected[-1]))
        final_recovered_last = int(np.round(final_recovered[-1]))
        
        children_dead = int(np.round(population.groups['Children']['dead']))
        young_adults_dead = int(np.round(population.groups['Young Adults']['dead']))
        middle_aged_dead = int(np.round(population.groups['Middle Aged']['dead']))
        senior_dead = int(np.round(population.groups['Senior']['dead']))
        
        final_dead_last = children_dead + young_adults_dead + middle_aged_dead + senior_dead

        max_infected_value, max_infected_day_value = max_infected_data[0]

        male_dead_total = 0
        female_dead_total = 0

        children_male_dead, children_female_dead = compute_group_gender_deaths(children_dead, population)
        young_adults_male_dead, young_adults_female_dead = compute_group_gender_deaths(young_adults_dead, population)
        middle_aged_male_dead, middle_aged_female_dead = compute_group_gender_deaths(middle_aged_dead, population)
        senior_male_dead, senior_female_dead = compute_group_gender_deaths(senior_dead, population)

        age_gender_deaths = {
            'Children': (children_male_dead, children_female_dead),
            'Young Adults': (young_adults_male_dead, young_adults_female_dead),
            'Middle Aged': (middle_aged_male_dead, middle_aged_female_dead),
            'Senior': (senior_male_dead, senior_female_dead)
        }

        male_dead_total = children_male_dead + young_adults_male_dead + middle_aged_male_dead + senior_male_dead
        female_dead_total = children_female_dead + young_adults_female_dead + middle_aged_female_dead + senior_female_dead

        (vaccine_inf_reduction_effect, vaccine_mort_reduction_effect,
         quarantine_inf_reduction_effect, quarantine_mort_reduction_effect) = population.calculate_effectiveness(
            vaccine_percent, quarantine_percent,
            vaccine_infection_reduction, vaccine_mortality_reduction,
            quarantine_infection_reduction, quarantine_mortality_reduction
        )

        male_total = int(np.round(population.total_population * (population.male_percent / 100)))
        female_total = population.total_population - male_total

        durations = population.average_infection_duration(
        gamma,
        vaccine_percent, vaccine_mortality_reduction,
        quarantine_percent, quarantine_mortality_reduction
        )

        os.makedirs("temp", exist_ok=True)
        with open(os.path.join("temp", "simulation_results.txt"), "w", encoding="utf-8") as file:
            file.write(f"Загальна кількість населення: {population.total_population}\n")
            file.write(f"Кількість чоловіків: {male_total}\n")
            file.write(f"Кількість жінок: {female_total}\n")
            file.write(f"Загальна кількість інфікованих (накопичено): {int(np.round(population.cumulative_infected))}\n")
            file.write(f"Кількість сприйнятливих (на кінець симуляції): {final_susceptible_last}\n")
            file.write(f"Кількість інфікованих (на кінець симуляції): {final_infected_last}\n")
            file.write(f"Кількість одужалих (на кінець симуляції): {final_recovered_last}\n")
            file.write(f"Кількість померлих (на кінець симуляції): {final_dead_last}\n")
            file.write(f"Максимальна кількість інфікованих за день: {int(np.round(max_infected_value))} в день {max_infected_day_value}\n")
            file.write("\nСмертність за статтю (загалом):\n")
            file.write(f"  Чоловіки: {male_dead_total}\n")
            file.write(f"  Жінки: {female_dead_total}\n")
            file.write("\nСмертність за віковими групами:\n")
            file.write("  Children:\n")
            file.write(f"    Загальна кількість: {children_dead}\n")
            file.write(f"    Померло хлопців: {children_male_dead}\n")
            file.write(f"    Померло дівчат: {children_female_dead}\n")
            file.write("  Young Adults:\n")
            file.write(f"    Загальна кількість: {young_adults_dead}\n")
            file.write(f"    Померло чоловіків: {young_adults_male_dead}\n")
            file.write(f"    Померло жінок: {young_adults_female_dead}\n")
            file.write("  Middle Aged:\n")
            file.write(f"    Загальна кількість: {middle_aged_dead}\n")
            file.write(f"    Померло чоловіків: {middle_aged_male_dead}\n")
            file.write(f"    Померло жінок: {middle_aged_female_dead}\n")
            file.write("  Senior:\n")
            file.write(f"    Загальна кількість: {senior_dead}\n")
            file.write(f"    Померло чоловіків: {senior_male_dead}\n")
            file.write(f"    Померло жінок: {senior_female_dead}\n")
            file.write("\nСередня тривалість інфекції:\n")
            for group, T in durations.items():
                file.write(f"  {group}: {T:.0f} дн. \n")
            vaccinated = int(np.round(population.total_population * vaccine_percent / 100))
            quarantined = int(np.round(population.total_population * quarantine_percent / 100))
            file.write(f"\nВакциновано: {vaccinated} осіб ({round(vaccine_percent, 2)}%)\n")
            file.write(f"Під карантином: {quarantined} осіб ({round(quarantine_percent, 2)}%)\n")
            file.write("\nЗменшення інфікування:\n")
            file.write(f"  - Завдяки вакцинації: {vaccine_inf_reduction_effect}%\n")
            file.write(f"  - Завдяки карантину: {quarantine_inf_reduction_effect}%\n")
            file.write("Зменшення смертності:\n")
            file.write(f"  - Завдяки вакцинації: {vaccine_mort_reduction_effect}%\n")
            file.write(f"  - Завдяки карантину: {quarantine_mort_reduction_effect}%\n")

        return {
            'susceptible': final_susceptible,
            'infected': final_infected,
            'recovered': final_recovered,
            'dead': final_dead,
            'age_deaths': final_age_deaths,
            'cumulative_infected': final_cumulative_infected,
            'population_gender': (male_total, female_total),
            'gender_deaths': (male_dead_total, female_dead_total),
            'age_gender_deaths': age_gender_deaths,
            'vaccine_quarantine_effects': (
                vaccine_inf_reduction_effect,
                vaccine_mort_reduction_effect,
                quarantine_inf_reduction_effect,
                quarantine_mort_reduction_effect
            ),
            'infection_durations': durations,
            'peak': (max_infected_value, max_infected_day_value)
        }
    else:
        return None
