#run_simulation.py
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from simulation import parallel_simulation
from visualisation import plot_results
from ui import SimulationApp

def start_simulation(population, beta, gamma, days):
    """
    Запуск симуляції з параметрами
    """
    num_processes = 8

    susceptible, infected, recovered = parallel_simulation(population, beta, gamma, days, num_processes)
    plot_results(susceptible, infected, recovered)
    
if __name__ == "__main__":
    app = SimulationApp()
    app.root.mainloop()