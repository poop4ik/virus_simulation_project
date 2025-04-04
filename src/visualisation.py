#visualisation.py
import matplotlib.pyplot as plt

def plot_results(susceptible, infected, recovered, save_path=None):
    """
    Функція для візуалізації результатів симуляції
    """
    days = range(len(susceptible))

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#f4f4f4")  # Змінюємо фон усієї фігури
    ax.set_facecolor("#f4f4f4")  # Змінюємо фон області графіка

    ax.plot(days, susceptible, label='Сприйнятливі', color='blue')
    ax.plot(days, infected, label='Заражені', color='red')
    ax.plot(days, recovered, label='Одужавші', color='green')

    ax.set_title("Симуляція поширення вірусу")
    ax.set_xlabel("Дні")
    ax.set_ylabel("Кількість людей")
    ax.legend()
    ax.grid(True)

    if save_path:
        plt.savefig(save_path, facecolor=fig.get_facecolor())  # Зберігаємо з урахуванням фону
    else:
        plt.show()

    plt.close()