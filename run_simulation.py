#run_simulation.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from ui import SimulationApp

if __name__ == "__main__":
    app = SimulationApp()
    app.root.mainloop()