from mpi4py import MPI
from model import run_sir_model
import numpy as np

def parallel_simulation(population, beta, gamma, days, num_processes):
    """
    Паралельна симуляція поширення вірусу за допомогою MPI
    """
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Розподіл робіт між процесами
    chunk_size = days // size
    start_day = rank * chunk_size
    end_day = (rank + 1) * chunk_size if rank != size - 1 else days

    # Виконання моделі для кожного процесу
    susceptible, infected, recovered = run_sir_model(population, beta, gamma, days)

    # Збір результатів з усіх процесів
    all_susceptible = comm.gather(susceptible[start_day:end_day], root=0)
    all_infected = comm.gather(infected[start_day:end_day], root=0)
    all_recovered = comm.gather(recovered[start_day:end_day], root=0)

    if rank == 0:
        # Об’єднання результатів на головному процесі
        final_susceptible = np.concatenate(all_susceptible)
        final_infected = np.concatenate(all_infected)
        final_recovered = np.concatenate(all_recovered)
        
        return final_susceptible, final_infected, final_recovered