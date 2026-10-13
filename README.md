# Habit Tracker

A command-line habit tracking backend written in Python. It combines an
**object-oriented** data model, a **functional-programming** analytics module and
**SQLite** persistence. Built for the course *Object Oriented and Functional
Programming with Python* (DLBDSOOFPP01), IU International University of Applied
Sciences.

## Features

- Create **daily** and **weekly** habits and check them off at any time (timestamped).
- Delete habits, with all their completions.
- Data is stored in SQLite and survives between sessions.
- Analytics: list all habits, list habits by periodicity, longest streak overall,
  longest streak for one habit, and the habits you struggled with most over the
  last 4 weeks.
- **5 predefined habits with 4 weeks of example data** are loaded automatically on
  first run (these are also the test fixtures).

## Requirements

- Python **3.7 or later**
- No third-party packages are needed to run the app (`sqlite3` is built into Python).
- `pytest` is only needed to run the tests.

## Installation

```bash
git clone https://github.com/biyimide/Habit_tracker_app.git
cd Habit_tracker_app

# optional but recommended: a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# only needed for the tests
pip install -r requirements-dev.txt
```

## Run the app

```bash
python main.py
```

The database file `habit_tracker.db` is created in the project folder on first run
and filled with the 5 predefined habits. To start over, delete that file.

### Using the menu

```
1. List all habits
2. Create a new habit
3. Check off a habit
4. List habits by periodicity (daily/weekly)
5. View longest streak overall
6. View longest streak for a specific habit
7. Delete a habit
8. Habits I struggled with most (last 4 weeks)
9. Exit
```

- **Create a habit (2):** enter a unique name, then `daily` or `weekly`.
- **Complete a task (3):** enter the habit's name (not case-sensitive). The current
  date and time are recorded. Checking off a habit several times in the same period
  is allowed but counts only once towards a streak.
- **Analyse (4, 5, 6, 8):** these options use the functions in `analytics/analytics.py`.

### How streaks work

A habit must be checked off at least once in every period; a period without a
check-off *breaks* the habit. A **daily** streak counts consecutive calendar days, a
**weekly** streak counts consecutive weeks (Monday to Sunday).

### Predefined habits (example data)

| Habit | Periodicity | Longest streak in example data |
|---|---|---|
| Drink 2L Water | daily | 7 days |
| Read 20 Pages | daily | 12 days |
| Meditate | daily | 10 days |
| Do Laundry | weekly | 2 weeks |
| Grocery Shopping | weekly | 4 weeks |

## Run the tests

```bash
python -m pytest
```

The tests cover habit creation and validation, completion, persistence, deletion,
every analytics function (including broken streaks, same-day duplicates, unsorted
data and weekly streaks) and the 4-week example data. Each test uses its own
temporary database, so your real data is never touched.

## Project structure

```
Habit_tracker_app/
├── main.py                  # CLI menu loop (entry point, no business logic)
├── models/
│   ├── habit.py             # Habit class (OOP core)
│   └── habit_manager.py     # Orchestrates habits and keeps SQLite in sync
├── analytics/
│   └── analytics.py         # Pure functions: filter, map, functools.reduce
├── db/
│   ├── database.py          # SQLite schema (habits, completions)
│   └── fixtures.py          # 5 predefined habits + 4 weeks of example data
├── tests/                   # pytest suite
├── requirements-dev.txt
└── README.md
```

## Design in short

| Layer | Responsibility |
|---|---|
| `Habit` | Holds one habit's state; knows nothing about storage or analysis. |
| `HabitManager` | The only code that talks to SQLite; the CLI calls only its methods. |
| `analytics` | Pure functions that take habit data in and return new data; nothing is mutated. |
| `main.py` | Reads input, calls one manager or analytics function per menu option. |

## License

See `LICENSE`.
