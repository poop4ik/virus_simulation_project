# Документація користувача

## 1. Запуск програми

1. Встановіть всі залежності:
   ```bash
   pip install -r requirements.txt
   ```
2. Перейдіть у корінь проєкту та запустіть головний скрипт:
   ```bash
   python run_simulation.py
   ```

## 2. Головне меню

Після запуску відкриється вікно з трьома кнопками:
- **Симуляція**: відкриває налаштування параметрів симуляції.
- **Обчислити параметри**: відкриває інтерфейс для розрахунку епідеміологічних коефіцієнтів.
- **Обчислити коефіцієнти**: обчислює коефіцієнти зараження та одужання.

## 3. Налаштування симуляції

1. Натисніть **Симуляція** → **Налаштування**.
2. Заповніть поля:
   - **Назва експерименту** — довільна назва (наприклад, `Test_Infection_X`).
   - **Популяція** — загальна кількість індивідів.
   - **% чоловіків / % жінок** — розподіл за статтю.
   - **% дітей (0–14), молоді (15–34), середнього віку (35–64), похилого (65+)**.
   - **Коеф. зараження (β)** — інтенсивність передачі інфекції.
   - **Коеф. одужання (γ)** — швидкість одужання.
   - **Кількість днів** — тривалість симуляції.
   - **Летальність за віковими групами (%)**.
   - **Смертність за статтю (%)**.
   - **Вакцинація (%) / Карантин (%)** — відсоток щеплених та ізольованих.
   - **↓ інфікування / ↓ смертність вакциною** — ефективність вакцинації.
   - **↓ інфікування / ↓ смертність карантином** — ефективність карантину.
3. Натисніть **Запустити симуляцію**.

### 3.1 Результати симуляції

- Зʼявиться повідомлення про успіх.
- Графіки відкриються або збережуться в папці `data/`.
- Параметри експерименту збережуться у файлі `data/simulation_parameters.txt`.

## 4. Обчислення параметрів

1. У головному меню натисніть **Обчислити параметри**.
2. Введіть:
   - Загальну популяцію та її розподіл.
   - Кількість інфікованих і померлих у кожній групі.
3. Натисніть **Обрахувати параметри** — результати з’являться у вікні.
4. Щоб зберегти, натисніть **Зберегти параметри** (файл `data/calculate_parameters.txt`).

## 5. Обчислення коефіцієнтів

1. У головному меню оберіть **Обчислити коефіцієнти**.
2. Введіть:
   - **Кількість контактів на день**.
   - **Ймовірність зараження при контакті** (0–1).
   - **Середню тривалість хвороби** (дні).
3. Натисніть **Обрахувати коефіцієнти** — отримаєте β та γ.
4. Для збереження натисніть **Зберегти коефіцієнти** (файл `data/calculate_factors.txt`).

## 6. Структура файлів

```
epidemic-simulation/
├── docs/
├── data/
│   ├── calculate_factors.txt
│   ├── calculate_parameters.txt
│   ├── charts_report.pdf
│   └── simulation_parameters.txt
├── fonts/
├── src/
│   ├── model.py
│   ├── save_results.py
│   ├── simulation.py
│   ├── ui.py
│   └── visualisation.py
├── temp/
├── README.md
├── USAGE.md
├── requirements.txt
└── run_simulation.py
```
