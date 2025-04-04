#model.py
import numpy as np

class Population:
    def __init__(self, total_population):
        self.total_population = total_population
        
        # Початкові значення для кожної групи
        self.male_percentage = 0.5  # 50% чоловіків
        self.female_percentage = 0.5  # 50% жінок
        
        # Вікові групи
        self.children_percentage = 0.2  # 20% дітей (0-14 років)
        self.young_adults_percentage = 0.3  # 30% молодих людей (15-34 роки)
        self.middle_age_percentage = 0.3  # 30% середнього віку (35-64 роки)
        self.senior_percentage = 0.2  # 20% похилого віку (65+ років)
        
        # Рахуємо кількість людей у кожній групі
        self.males = self.total_population * self.male_percentage
        self.females = self.total_population * self.female_percentage
        self.children = self.total_population * self.children_percentage
        self.young_adults = self.total_population * self.young_adults_percentage
        self.middle_aged = self.total_population * self.middle_age_percentage
        self.senior = self.total_population * self.senior_percentage

    def get_group_data(self):
        return {
            "Males": self.males,
            "Females": self.females,
            "Children": self.children,
            "Young Adults": self.young_adults,
            "Middle Aged": self.middle_aged,
            "Senior": self.senior
        }


def run_sir_model(population, beta, gamma, days):
    susceptible = population.total_population - 1  # Використовуємо атрибут total_population
    infected = 1  # Початкова кількість інфікованих
    recovered = 0  # Початкова кількість одужавших

    susceptible_list = [susceptible]
    infected_list = [infected]
    recovered_list = [recovered]

    for day in range(1, days + 1):
        new_infected = beta * susceptible * infected / population.total_population
        new_recovered = gamma * infected

        susceptible -= new_infected
        infected += new_infected - new_recovered
        recovered += new_recovered

        susceptible_list.append(susceptible)
        infected_list.append(infected)
        recovered_list.append(recovered)

    return susceptible_list, infected_list, recovered_list