import numpy as np

class Population:
    def __init__(self, total_population, children_percent, young_adults_percent, middle_age_percent, senior_percent):
        self.total_population = total_population
        
        # Обчислюємо чисельність кожної вікової групи на основі відсотків
        self.children = int(total_population * children_percent)
        self.young_adults = int(total_population * young_adults_percent)
        self.middle_aged = int(total_population * middle_age_percent)
        self.senior = int(total_population * senior_percent)

        # Створюємо словник з детальною інформацією
        self.group_data = {
            "Children": {
                "count": self.children,
                "percentage": children_percent
            },
            "Young Adults": {
                "count": self.young_adults,
                "percentage": young_adults_percent
            },
            "Middle Aged": {
                "count": self.middle_aged,
                "percentage": middle_age_percent
            },
            "Senior": {
                "count": self.senior,
                "percentage": senior_percent
            }
        }

    def get_group_data(self):
        return self.group_data

    def get_total_population(self):
        return self.total_population


def run_sir_model(population_obj, beta, gamma, days,
                  death_rate_children, death_rate_young_adults, death_rate_middle_age, death_rate_senior):
    """
    Модель поширення вірусу з урахуванням вакцинації та карантину.
    """

    population = population_obj.total_population

    # Ініціалізація масивів для збереження результатів
    susceptible = np.zeros(days)
    infected = np.zeros(days)
    recovered = np.zeros(days)
    deaths = np.zeros(days)

    # Початкові значення
    susceptible[0] = population - 1
    infected[0] = 1
    recovered[0] = 0

    # Симуляція
    for day in range(1, days):
        new_infected = beta * susceptible[day - 1] * infected[day - 1] / population
        new_recovered = gamma * infected[day - 1]

        susceptible[day] = susceptible[day - 1] - new_infected
        infected[day] = infected[day - 1] + new_infected - new_recovered
        recovered[day] = recovered[day - 1] + new_recovered

        # Додаємо смертність для кожної вікової групи
        deaths[day] = (
            death_rate_children * population_obj.children * infected[day] / population +
            death_rate_young_adults * population_obj.young_adults * infected[day] / population +
            death_rate_middle_age * population_obj.middle_aged * infected[day] / population +
            death_rate_senior * population_obj.senior * infected[day] / population
        )

    return susceptible, infected, recovered, deaths
