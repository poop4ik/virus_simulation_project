#simulatiom.py
from mpi4py import MPI
from model import run_sir_model, Population
import numpy as np

def parallel_simulation(population_obj, beta, gamma, days, children_percent, young_adults_percent, middle_age_percent, senior_percent, 
                         death_rate_children, death_rate_young_adults, death_rate_middle_age, death_rate_senior, 
                         vaccination, quarantine, vaccine_infection_reduction, vaccine_mortality_reduction, 
                         quarantine_infection_reduction, quarantine_mortality_reduction, num_processes):

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    population = population_obj

    # Розподіл роботи між процесами
    chunk_size = days // size
    start_day = rank * chunk_size
    end_day = (rank + 1) * chunk_size if rank != size - 1 else days
    
    if vaccination > 0:
        # Знижуємо загальну ймовірність зараження на основі вакцинації
        beta *= (1 - vaccination)  # Знижуємо ймовірність зараження в залежності від відсотка вакцинації
    
    if quarantine > 0:
        # Знижуємо загальну ймовірність зараження на основі карантину
        beta *= (1 - quarantine)  # Знижуємо ймовірність зараження в залежності від карантину
    
    vaccination_impact = 100 * (vaccine_infection_reduction * vaccination)
    vaccination_mortality_impact = 100 * (vaccine_mortality_reduction * vaccination)

    quarantine_impact = 100 * (quarantine_infection_reduction * quarantine)
    quarantine_mortality_impact = 100 * (quarantine_mortality_reduction * quarantine)

    susceptible, infected, recovered, deaths = run_sir_model(
        population, beta, gamma, days,
        death_rate_children, death_rate_young_adults, death_rate_middle_age, death_rate_senior
    )

    # Обчислення смертності
    children_mortality = death_rate_children * population.children
    young_adults_mortality = death_rate_young_adults * population.young_adults
    middle_age_mortality = death_rate_middle_age * population.middle_aged
    senior_mortality = death_rate_senior * population.senior
    total_mortality = children_mortality + young_adults_mortality + middle_age_mortality + senior_mortality

    # Збір результатів
    all_susceptible = comm.gather(susceptible[start_day:end_day], root=0)
    all_infected = comm.gather(infected[start_day:end_day], root=0)
    all_recovered = comm.gather(recovered[start_day:end_day], root=0)
    all_deaths = comm.gather(deaths[start_day:end_day], root=0)

    if rank == 0:
        final_susceptible = np.concatenate(all_susceptible)
        final_infected = np.concatenate(all_infected)
        final_recovered = np.concatenate(all_recovered)
        final_deaths = np.concatenate(all_deaths)
    
        # Зменшуємо інфікованих відповідно до впливу вакцинації та карантину
        final_infected *= (1 - vaccination_impact / 100)  # Зменшуємо інфікованих на основі вакцинації
        final_infected *= (1 - quarantine_impact / 100)  # Зменшуємо інфікованих через карантин
    
        # Зменшуємо смертність для кожної вікової групи
        children_mortality = children_mortality * (1 - vaccination_mortality_impact / 100) * (1 - quarantine_mortality_impact / 100)
        young_adults_mortality = young_adults_mortality * (1 - vaccination_mortality_impact / 100) * (1 - quarantine_mortality_impact / 100)
        middle_age_mortality = middle_age_mortality * (1 - vaccination_mortality_impact / 100) * (1 - quarantine_mortality_impact / 100)
        senior_mortality = senior_mortality * (1 - vaccination_mortality_impact / 100) * (1 - quarantine_mortality_impact / 100)
    
        # Підсумкова смертність
        total_mortality = children_mortality + young_adults_mortality + middle_age_mortality + senior_mortality
    
        return final_susceptible, final_infected, final_recovered, final_deaths, total_mortality, \
               children_mortality, young_adults_mortality, middle_age_mortality, senior_mortality, \
               vaccination_impact, vaccination_mortality_impact, quarantine_impact, quarantine_mortality_impact
    