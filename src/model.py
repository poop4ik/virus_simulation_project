import numpy as np

def run_sir_model(population, beta, gamma, days):
    """
    Функція для запуску моделі SIR
    population: загальна кількість людей
    beta: ймовірність зараження
    gamma: ймовірність одужання
    days: кількість днів для симуляції
    """

    # Ініціалізація початкових значень
    susceptible = population - 1
    infected = 1
    recovered = 0

    # Списки для зберігання результатів
    susceptible_list = []
    infected_list = []
    recovered_list = []

    for day in range(days):
        # Додавання значень до списків
        susceptible_list.append(susceptible)
        infected_list.append(infected)
        recovered_list.append(recovered)

        # Обчислення нових значень
        new_infected = beta * susceptible * infected / population
        new_recovered = gamma * infected

        susceptible -= new_infected
        infected += new_infected - new_recovered
        recovered += new_recovered

    return susceptible_list, infected_list, recovered_list