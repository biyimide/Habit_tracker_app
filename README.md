# Habit_tracker_app
CLI App using object-oriented and functional python programming
# Python Habit Tracking App Backend

A robust command-line habit tracking application built with **Python**, combining an **Object-Oriented Programming (OOP)** core domain model, a **functional programming analytics module**, and **SQLite data persistence**.

---

## 🚀 Project Overview
This project was developed as part of the Object-Oriented and Functional Programming with Python course. The application allows users to define daily and weekly habits, check them off, record timestamps, persist data between sessions, and analyze execution consistency through functional analytics routines.

---

## 🛠️ Tech Stack & Architecture
* **Language:** Python 3.7+
* **Data Model (OOP):** Encapsulated `Habit` class handling task creation, period validations, and completion states.
* **Orchestration:** `HabitManager` class managing runtime states and synchronizing actions.
* **Analytics Engine (Functional Programming):** Pure functions utilizing higher-order functions (`filter`, `map`, `functools.reduce`) to calculate consistency metrics and streak lengths without mutating state.
* **Persistence Layer:** Relational database management using Python's built-in `sqlite3` module (`habits` and `completions` normalized tables).
* **Interface:** Interactive Command Line Interface (CLI) loop via `main.py`.

---

## 📂 Project Directory Structure
```text
habit_tracker_app/
│
├── analytics/
│   ├── __init__.py
│   └── analytics.py       # Pure functions for functional analytics & streak calculations
│
├── db/
│   ├── __init__.py
│   └── database.py        # SQLite schema initialization and table creation
│
├── models/
│   ├── __init__.py
│   ├── habit.py           # Core Habit class (OOP encapsulation)
│   └── habit_manager.py   # Orchestrator linking CLI, DB, and models
│
├── main.py                # Interactive CLI menu loop and application entry point
└── README.md              # Project documentation and run instructions
