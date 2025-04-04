#save_results.py
import numpy as np 
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import matplotlib.pyplot as plt
import os

RESULTS_DIR = "data"

def save_results_to_pdf(experiment_name, population, beta, gamma, days, susceptible, infected, recovered):
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)

    pdf_path = os.path.join(RESULTS_DIR, f"{experiment_name}.pdf")
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setFont("Times-Roman", 12)

    # Текст у PDF англійською
    c.drawString(50, 750, f"Experiment: {experiment_name}")
    c.drawString(50, 730, f"Population: {population}, β: {beta}, γ: {gamma}, Days: {days}")

    max_infected = int(np.max(infected))
    peak_day = int(np.argmax(infected))  
    total_infected = int(np.sum(infected))  


    c.drawString(50, 700, f"Max infected: {max_infected} on day {peak_day}")
    c.drawString(50, 680, f"Total infected during the period: {total_infected}")
    
    # Збереження графіка (українські підписи)
    graph_path = os.path.join(RESULTS_DIR, f"{experiment_name}.png")
    plt.figure(figsize=(6, 4))
    plt.plot(range(days), susceptible, label="Сприйнятливі", color="blue")
    plt.plot(range(days), infected, label="Інфіковані", color="red")
    plt.plot(range(days), recovered, label="Одужалі", color="green")
    plt.xlabel("Дні")
    plt.ylabel("Люди")
    plt.legend()
    plt.grid()
    plt.title("Динаміка поширення вірусу")
    plt.savefig(graph_path)
    plt.close()

    # Додавання зображення в PDF
    c.drawImage(graph_path, 50, 375, width=500, height=300)
    c.save()

    print(f"Results saved in {pdf_path}")