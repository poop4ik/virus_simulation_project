#model.py
import numpy as np
import random

class Population:
    def __init__(self, total_population, children_percentage, young_adults_percentage, 
                 middle_age_percentage, senior_percentage,
                 death_rate_children, death_rate_young_adults, death_rate_middle_age, death_rate_senior,
                 male_percent, female_percent, male_mortality, female_mortality):
        self.total_population = total_population
        self.male_percent = male_percent
        self.female_percent = female_percent
        self.male_mort_rate = male_mortality
        self.female_mort_rate = female_mortality
        self.cumulative_infected = 0

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
        
        initial_infected = 10 

        for _ in range(initial_infected):
            eligible_groups = [group for group in self.groups if self.groups[group]["susceptible"] > 0]

            if eligible_groups:
                chosen_group = random.choice(eligible_groups)
                self.groups[chosen_group]["infected"] += 1  # додаємо одного інфікованого до групи
                self.groups[chosen_group]["susceptible"] -= 1  # зменшуємо кількість сприйнятливих
                self.cumulative_infected += 1  # рахуємо загальну кількість інфікованих


    def simulate_day(self, beta, gamma, vaccine_percent, vaccine_infection_reduction, vaccine_mortality_reduction,
                     quarantine_percent, quarantine_infection_reduction, quarantine_mortality_reduction):
        local_results = {}
        v_cov = vaccine_percent / 100
        q_cov = quarantine_percent / 100

        v_inf_eff = vaccine_infection_reduction / 100  
        q_inf_eff = quarantine_infection_reduction / 100  
        v_mort_eff = vaccine_mortality_reduction / 100  
        q_mort_eff = quarantine_mortality_reduction / 100  

        reduction_inf = v_inf_eff * v_cov + q_inf_eff * q_cov
        effective_beta = beta * max(1 - reduction_inf, 0)

        total_infected = sum(data["infected"] for data in self.groups.values())

        for group, data in self.groups.items():
            s = data["susceptible"]
            i = data["infected"]
            r = data["recovered"]
            d = data["dead"]
            total = data["total"]
            mortality_rate = data["mortality_rate"]

            reduction_mort = v_mort_eff * v_cov + q_mort_eff * q_cov
            effective_mort_rate = mortality_rate * max(1 - reduction_mort, 0)

            new_infected = effective_beta * s * total_infected / self.total_population if self.total_population > 0 else 0

            new_recovered = gamma * i
            new_dead = (effective_mort_rate / 100) * i

            self.cumulative_infected += new_infected

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

            self.groups[group]["susceptible"] = s_new
            self.groups[group]["infected"] = i_new
            self.groups[group]["recovered"] = r_new
            self.groups[group]["dead"] = d_new

        return local_results

    def calculate_effectiveness(self, vaccine_percent, quarantine_percent,
                                vaccine_infection_reduction, vaccine_mortality_reduction,
                                quarantine_infection_reduction, quarantine_mortality_reduction):
        v_cov = vaccine_percent / 100
        q_cov = quarantine_percent / 100

        v_inf_eff = vaccine_infection_reduction / 100
        q_inf_eff = quarantine_infection_reduction / 100
        v_mort_eff = vaccine_mortality_reduction / 100
        q_mort_eff = quarantine_mortality_reduction / 100

        vaccine_inf_reduction_effect = round(v_inf_eff * v_cov * 100, 2)
        vaccine_mort_reduction_effect = round(v_mort_eff * v_cov * 100, 2)
        quarantine_inf_reduction_effect = round(q_inf_eff * q_cov * 100, 2)
        quarantine_mort_reduction_effect = round(q_mort_eff * q_cov * 100, 2)

        return (vaccine_inf_reduction_effect, vaccine_mort_reduction_effect,
                quarantine_inf_reduction_effect, quarantine_mort_reduction_effect)
    
    def average_infection_duration(self, gamma,
                                   vaccine_percent, vaccine_mortality_reduction,
                                   quarantine_percent, quarantine_mortality_reduction):
        v_cov = vaccine_percent / 100
        q_cov = quarantine_percent / 100
        v_mort_eff = vaccine_mortality_reduction / 100
        q_mort_eff = quarantine_mortality_reduction / 100

        reduction_mort = v_mort_eff * v_cov + q_mort_eff * q_cov

        durations = {}
        for group, data in self.groups.items():
            μ = data["mortality_rate"] * (1 - reduction_mort) / 100 
            removal_rate = gamma + μ
            T = (1 / removal_rate) if removal_rate > 0 else float('inf')
            durations[group] = int(round(T))
        return durations
