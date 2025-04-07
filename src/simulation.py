from mpi4py import MPI 
import numpy as np
from model import Population

def parallel_simulation(population, beta, gamma, days, num_processes,
                        vaccine_percent, vaccine_infection_reduction, vaccine_mortality_reduction,
                        quarantine_percent, quarantine_infection_reduction, quarantine_mortality_reduction):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Розподіл днів для кожного процесу
    chunk_size = days // size
    start_day = rank * chunk_size
    end_day = (rank + 1) * chunk_size if rank != size - 1 else days

    local_results = {
        'susceptible': np.zeros(days),
        'infected': np.zeros(days),
        'recovered': np.zeros(days),
        'dead': np.zeros(days)
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

        if local_results['infected'][day] > max_infected:
            max_infected = local_results['infected'][day]
            max_infected_day = day

    gathered_results = comm.gather(local_results, root=0)
    max_infected_data = comm.gather((max_infected, max_infected_day), root=0)

    if rank == 0:
        final_susceptible = np.zeros(days)
        final_infected = np.zeros(days)
        final_recovered = np.zeros(days)
        final_dead = np.zeros(days)

        for result in gathered_results:
            final_susceptible += result['susceptible']
            final_infected += result['infected']
            final_recovered += result['recovered']
            final_dead += result['dead']

        final_susceptible_last = int(np.round(final_susceptible[-1]))
        final_infected_last = int(np.round(final_infected[-1]))
        final_recovered_last = int(np.round(final_recovered[-1]))
        
        # Отримання кількості смертей за кожною віковою групою безпосередньо з даних груп
        children_dead = int(np.round(population.groups['Children']['dead']))
        young_adults_dead = int(np.round(population.groups['Young Adults']['dead']))
        middle_aged_dead = int(np.round(population.groups['Middle Aged']['dead']))
        senior_dead = int(np.round(population.groups['Senior']['dead']))
        
        # Сумарна кількість смертей дорівнює сумі смертей по групах
        final_dead_last = children_dead + young_adults_dead + middle_aged_dead + senior_dead

        max_infected_value, max_infected_day_value = max_infected_data[0]

        # Підрахунок смертності за статтю
        male_dead = int(np.round(population.male_percent / 100 * final_dead_last))
        female_dead = final_dead_last - male_dead 

        # Розподіл смертності за віковими групами із корекцією за статтю
        male_dead_children = int(np.round(children_dead * population.male_percent / 100))
        female_dead_children = children_dead - male_dead_children

        male_dead_young_adults = int(np.round(young_adults_dead * population.male_percent / 100))
        female_dead_young_adults = young_adults_dead - male_dead_young_adults

        male_dead_middle_aged = int(np.round(middle_aged_dead * population.male_percent / 100))
        female_dead_middle_aged = middle_aged_dead - male_dead_middle_aged

        male_dead_senior = int(np.round(senior_dead * population.male_percent / 100))
        female_dead_senior = senior_dead - male_dead_senior

        # Запис результатів у файл
        with open("simulation_results.txt", "w", encoding="utf-8") as file:
            file.write(f"Загальна кількість населення: {population.total_population}\n")
            file.write(f"Загальна кількість інфікованих (накопичено): {int(np.round(final_infected[-1]))}\n")
            file.write(f"Кількість сприйнятливих (на кінець симуляції): {final_susceptible_last}\n")
            file.write(f"Кількість інфікованих (на кінець симуляції): {final_infected_last}\n")
            file.write(f"Кількість одужалих (на кінець симуляції): {final_recovered_last}\n")
            file.write(f"Кількість померлих (на кінець симуляції): {final_dead_last}\n")
            file.write(f"Максимальна кількість інфікованих за день: {int(np.round(max_infected))} в день {max_infected_day_value}\n")

            file.write(f"\nСмертність за статтю:\nЧоловіки: {male_dead}\nЖінки: {female_dead}\n")

            file.write(f"\nСмертність за віковими групами:\n")
            file.write(f"Children: {children_dead} (Чоловіки: {male_dead_children}, Жінки: {female_dead_children})\n")
            file.write(f"Young Adults: {young_adults_dead} (Чоловіки: {male_dead_young_adults}, Жінки: {female_dead_young_adults})\n")
            file.write(f"Middle Aged: {middle_aged_dead} (Чоловіки: {male_dead_middle_aged}, Жінки: {female_dead_middle_aged})\n")
            file.write(f"Senior: {senior_dead} (Чоловіки: {male_dead_senior}, Жінки: {female_dead_senior})\n")

            # Дані щодо вакцинації та карантину
            vaccinated = int(np.round(population.total_population * vaccine_percent / 100))
            quarantined = int(np.round(population.total_population * quarantine_percent / 100))

            file.write(f"\nВакциновано: {vaccinated} осіб ({vaccine_percent}%)\n")
            file.write(f"Під карантином: {quarantined} осіб ({quarantine_percent}%)\n")

            vaccine_inf_reduction = round(vaccine_infection_reduction * (vaccine_percent / 100), 2)
            vaccine_mort_reduction = round(vaccine_mortality_reduction * (vaccine_percent / 100), 2)
            quarantine_inf_reduction = round(quarantine_infection_reduction * (quarantine_percent / 100), 2)
            quarantine_mort_reduction = round(quarantine_mortality_reduction * (quarantine_percent / 100), 2)

            file.write(f"\nЗменшення інфікування:\n - Завдяки вакцинації: {vaccine_inf_reduction}%\n")
            file.write(f" - Завдяки карантину: {quarantine_inf_reduction}%\n")
            file.write(f"Зменшення смертності:\n - Завдяки вакцинації: {vaccine_mort_reduction}%\n")
            file.write(f" - Завдяки карантину: {quarantine_mort_reduction}%\n")

        return final_susceptible, final_infected, final_recovered, final_dead
    else:
        return None, None, None, None
