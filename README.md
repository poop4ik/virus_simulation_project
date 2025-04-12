# Симуляція епідемії з MPI та графічним інтерфейсом Tkinter

Цей проєкт реалізує інструмент для симуляції поширення інфекційного захворювання серед населення з урахуванням розподілу за віком та статтю, ефектів вакцинації та карантину, а також змінної тривалості інфекції. Обчислення можуть виконуватись паралельно за допомогою MPI (`mpi4py`), а графічний інтерфейс побудований на Tkinter для налаштування параметрів, запуску симуляції та збереження результатів. Візуалізації створюються за допомогою Matplotlib та експортуються у PDF через ReportLab.

## Особливості проєкту

- **Паралельна симуляція**: розподіл обчислень між процесами за допомогою MPI (`mpi4py`).
- **Демографічне моделювання**: стратифікація населення за віковими групами (діти, молоді дорослі, дорослі, літні) та статтю.
- **Вакцинація та карантин**: моделювання впливу рівня вакцинації та карантинних заходів на захворюваність та смертність.
- **Налаштовувані параметри**: можливість задавати коефіцієнти інфекції (`beta`), одужання (`gamma`), ефективність вакцинації та карантину, тривалість симуляції.
- **Інтерактивний GUI**: за допомогою Tkinter можна:
  - Налаштувати параметри симуляції
  - Обчислити та зберегти епідеміологічні параметри
  - Запустити симуляцію та спостерігати прогрес
  - Зберегти параметри та результати у текстовий файл або PDF
- **Візуалізації**:
  - Кількість сприйнятливих, інфікованих, тих, що одужали, і загиблих з часом
  - Розподіл за статтю та смертність за статтю
  - Смертність за віковими групами та розподіл за віком і статтю
  - Вплив вакцинації та карантину
  - Кумулятивна кількість інфікованих та день піку
  - Тривалість інфекції у різних випадках
- **Експорт результатів**: генерування PDF-звітів з результатами та графіками за допомогою ReportLab.

## Встановлення

1. **Клонування репозиторію**:
   ```bash
   git clone https://github.com/yourusername/epidemic-simulation.git
   cd epidemic-simulation
   ```

2. **Встановлення залежностей**:
   ```bash
   pip install -r requirements.txt
   ```

   У файлі `requirements.txt` мають бути:
   ```txt
   mpi4py
   matplotlib
   numpy
   scipy
   reportlab
   tk
   ```

## Запуск

1. **Запуск графічного інтерфейсу**:
   ```bash
   python run_simulation.py
   ```

2. **У графічному інтерфейсі**:
   - Перейдіть у меню налаштувань симуляції та введіть параметри
   - За потреби обчисліть епідеміологічні коефіцієнти
   - Натисніть «Запустити симуляцію» та спостерігайте за ходом у консолі
   - Після завершення перегляньте або збережіть результати та графіки

3. **Запуск із коду (для просунутих користувачів)**:
   ```python
   from simulation import parallel_simulation
   from model import Population

   pop = Population(total_population=10000, children_percentage=0.2, young_adults_percentage=0.3, ...)
   results = parallel_simulation(population=pop, beta=0.3, gamma=0.1, days=160, num_processes=4)
   ```

## Структура файлів

```
eepidemic-simulation/
├── docs/                   # документація та інші довідкові матеріали
├── data/                   # вхідні/вихідні дані (наприклад, `calculate_factors.txt`, `simulation_parameter.txt`, `charts_report.pdf` тощо)
├── fonts/                  # шрифти (наприклад, `Royal_Arial.ttf`)
├── src/                    # вихідний код
│   ├── __pycache__/        # кешовані Python файли
│   ├── __init__.py
│   ├── model.py
│   ├── save_results.py
│   ├── simulation.py
│   ├── ui.py
│   └── visualisation.py
├── temp/                   # тимчасові файли та результати (графіки, текстові звіти тощо)
├── README.md               # документація проєкту
├── requirements.txt        # залежності Python
└── run_simulation.py       # точка входу для GUI-додатку
```

## Ліцензія

Цей проєкт ліцензовано за умовами MIT License. Докладніше — у файлі [LICENSE](LICENSE).
