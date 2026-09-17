from datetime import datetime
from typing import List
import sqlite3
from models.habit import Habit

class HabitManager:
    def __init__(self, db_path: str = "habit_tracker.db"):
        self.db_path = db_path
        self.habits: List[Habit] = []
        self.load_habits()

    def load_habits(self) -> None:
        """Loads all habits and their completions from the SQLite database."""
        self.habits = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, periodicity, created_at FROM habits;")
            habit_rows = cursor.fetchall()

            for row in habit_rows:
                h_id, name, periodicity, created_at = row
                habit = Habit(
                    name=name,
                    periodicity=periodicity,
                    created_at=datetime.fromisoformat(created_at),
                    habit_id=h_id
                )

                # Load completion timestamps for this habit
                cursor.execute("SELECT completed_at FROM completions WHERE habit_id = ?;", (h_id,))
                comp_rows = cursor.fetchall()
                for comp_row in comp_rows:
                    habit.completions.append(datetime.fromisoformat(comp_row[0]))

                self.habits.append(habit)

    def create_habit(self, name: str, periodicity: str) -> Habit:
        """Creates a new habit, saves it to the database, and adds it to memory."""
        created_at = datetime.now()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO habits (name, periodicity, created_at) VALUES (?, ?, ?);",
                (name, periodicity, created_at.isoformat())
            )
            conn.commit()
            habit_id = cursor.lastrowid

        new_habit = Habit(name, periodicity, created_at, habit_id)
        self.habits.append(new_habit)
        return new_habit

    def complete_habit(self, name: str) -> bool:
        """Checks off a habit by name and saves the completion to the database."""
        for habit in self.habits:
            if habit.name.lower() == name.lower():
                now = datetime.now()
                habit.complete(now)
                
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO completions (habit_id, completed_at) VALUES (?, ?);",
                        (habit.id, now.isoformat())
                    )
                    conn.commit()
                return True
        return False