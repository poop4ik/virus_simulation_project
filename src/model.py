import numpy as np

class Population:
    def __init__(self, total_population, children_percentage, young_adults_percentage, 
                 middle_age_percentage, senior_percentage,
                 death_rate_children, death_rate_young_adults, death_rate_middle_age, death_rate_senior,
                 male_percent, female_percent):
        self.total_population = total_population
        self.male_percent = male_percent
        self.female_percent = female_percent

        # Дані для кожної вікової групи
        self.groups = {
            "Children": {
                "percentage": children_percentage,
                "total": int(total_population * children_percentage / 100),
                "mortality_rate": death_rate_children,
                "susceptible": int(total_population * children_percentage / 100),
                "infected": 0,
                "recovered": 0,
                "dead": 0
            },
            "Young Adults": {
                "percentage": young_adults_percentage,
                "total": int(total_population * young_adults_percentage / 100),
                "mortality_rate": death_rate_young_adults,
                "susceptible": int(total_population * young_adults_percentage / 100),
                "infected": 0,
                "recovered": 0,
                "dead": 0
            },
            "Middle Aged": {
                "percentage": middle_age_percentage,
                "total": int(total_population * middle_age_percentage / 100),
                "mortality_rate": death_rate_middle_age,
                "susceptible": int(total_population * middle_age_percentage / 100),
                "infected": 0,
                "recovered": 0,
                "dead": 0
            },
            "Senior": {
                "percentage": senior_percentage,
                "total": int(total_population * senior_percentage / 100),
                "mortality_rate": death_rate_senior,
                "susceptible": int(total_population * senior_percentage / 100),
                "infected": 0,
                "recovered": 0,
                "dead": 0
            }
        }
        # Початкове зараження: по одному зараженому в кожній групі
        for group in self.groups:
            if self.groups[group]["susceptible"] > 0:
                self.groups[group]["infected"] = 1
                self.groups[group]["susceptible"] -= 1

    def simulate_day(self, beta, gamma, vaccine_percent, vaccine_infection_reduction, vaccine_mortality_reduction,
                     quarantine_percent, quarantine_infection_reduction, quarantine_mortality_reduction):
        local_results = {}
        for group, data in self.groups.items():
            s = data["susceptible"]
            i = data["infected"]
            r = data["recovered"]
            d = data["dead"]
            total = data["total"]
            mortality_rate = data["mortality_rate"]
    
            # Розрахунок нових заражень, одужань і смертей
            new_infected = beta * s * i / total if total > 0 else 0
            new_recovered = gamma * i
            new_dead = (mortality_rate / 100) * i
    
            s_new = s - new_infected
            i_new = i + new_infected - new_recovered - new_dead
            r_new = r + new_recovered
            d_new = d + new_dead
    
            local_results[group] = {
                "susceptible": s_new,
                "infected": i_new,
                "recovered": r_new,
                "dead": d_new
            }
    
            # Оновлення даних групи для наступного дня
            self.groups[group]["susceptible"] = s_new
            self.groups[group]["infected"] = i_new
            self.groups[group]["recovered"] = r_new
            self.groups[group]["dead"] = d_new
    
        return local_results
    

    def calculate_effectiveness(self, vaccine_percent, quarantine_percent,
                                vaccine_infection_reduction, vaccine_mortality_reduction,
                                quarantine_infection_reduction, quarantine_mortality_reduction):
        v_coverage = vaccine_percent / 100
        q_coverage = quarantine_percent / 100

        vaccine_inf_reduction = round(vaccine_infection_reduction * v_coverage, 2)
        vaccine_mort_reduction = round(vaccine_mortality_reduction * v_coverage, 2)

        quarantine_inf_reduction = round(quarantine_infection_reduction * q_coverage, 2)
        quarantine_mort_reduction = round(quarantine_mortality_reduction * q_coverage, 2)

        return vaccine_inf_reduction, vaccine_mort_reduction, quarantine_inf_reduction, quarantine_mort_reduction
