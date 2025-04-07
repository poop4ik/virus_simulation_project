import numpy as np
import matplotlib.pyplot as plt

def plot_results(susceptible, infected, recovered, dead):
    days = range(len(susceptible))  # Припускаємо, що всі масиви однакової довжини

    plt.figure(figsize=(10, 6))

    plt.plot(days, susceptible, label='Susceptible', color='blue')
    plt.plot(days, infected, label='Infected', color='red')
    plt.plot(days, recovered, label='Recovered', color='green')
    plt.plot(days, dead, label='Dead', color='black')

    plt.xlabel('Days')
    plt.ylabel('Population')
    plt.title('Epidemic Simulation Results')
    plt.legend()
    plt.grid(True)

    plt.show()
