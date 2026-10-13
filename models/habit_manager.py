"""HabitManager: sits between the CLI and the storage layer."""
import sqlite3
from datetime import datetime
from typing import List, Optional

from models.habit import Habit


class HabitManager:
    """Holds the in-memory habits and keeps them in sync with SQLite.

    Every mutation (create, complete, delete) is written to the database
    immediately, so data survives between sessions. The database tables must
    already exist; call db.database.init_db() first.
    """

    def __init__(self, db_path: str = "habit_tracker.db"):
        """Open the manager and load all habits from the database.

        Args:
            db_path: Path of the SQLite database file.
        """
        self.db_path = db_path
        self.habits: List[Habit] = []
        self.load_habits()

    def _connect(self) -> sqlite3.Connection:
        """Open a connection with foreign-key enforcement switched on."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def load_habits(self) -> None:
        """Replace the in-memory list with habits and completions from the DB."""
        self.habits = []
        conn = self._connect()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, periodicity, created_at FROM habits "
                "ORDER BY id;")
            for h_id, name, periodicity, created_at in cursor.fetchall():
                habit = Habit(name, periodicity,
                              datetime.fromisoformat(created_at), h_id)
                cursor.execute(
                    "SELECT completed_at FROM completions "
                    "WHERE habit_id = ? ORDER BY completed_at;", (h_id,))
                habit.completions = [datetime.fromisoformat(row[0])
                                     for row in cursor.fetchall()]
                self.habits.append(habit)
        finally:
            conn.close()

    def list_habits(self) -> List[Habit]:
        """Return a copy of the list of all tracked habits."""
        return list(self.habits)

    def get_habit(self, name: str) -> Optional[Habit]:
        """Find a habit by name (case-insensitive); None if it does not exist."""
        wanted = name.strip().lower()
        return next((h for h in self.habits if h.name.lower() == wanted), None)

    def create_habit(self, name: str, periodicity: str,
                     created_at: Optional[datetime] = None) -> Habit:
        """Create a habit, store it in the database and add it to memory.

        Args:
            name: Task specification (must be unique, case-insensitive).
            periodicity: "daily" or "weekly".
            created_at: Creation timestamp. Defaults to now.

        Raises:
            ValueError: If the input is invalid or the name already exists.
        """
        habit = Habit(name, periodicity, created_at)
        if self.get_habit(habit.name) is not None:
            raise ValueError("A habit named '{}' already exists.".format(habit.name))

        conn = self._connect()
        try:
            cursor = conn.execute(
                "INSERT INTO habits (name, periodicity, created_at) "
                "VALUES (?, ?, ?);",
                (habit.name, habit.periodicity, habit.created_at.isoformat()))
            conn.commit()
            habit.id = cursor.lastrowid
        finally:
            conn.close()

        self.habits.append(habit)
        return habit

    def complete_habit(self, name: str,
                       timestamp: Optional[datetime] = None) -> bool:
        """Check a habit off and store the completion.

        Args:
            name: Name of the habit (case-insensitive).
            timestamp: Completion time. Defaults to now.

        Returns:
            True if the habit exists and was checked off, otherwise False.
        """
        habit = self.get_habit(name)
        if habit is None:
            return False

        moment = timestamp or datetime.now()
        habit.complete(moment)
        conn = self._connect()
        try:
            conn.execute(
                "INSERT INTO completions (habit_id, completed_at) VALUES (?, ?);",
                (habit.id, moment.isoformat()))
            conn.commit()
        finally:
            conn.close()
        return True

    def delete_habit(self, name: str) -> bool:
        """Delete a habit and all of its completions.

        Returns:
            True if the habit existed and was deleted, otherwise False.
        """
        habit = self.get_habit(name)
        if habit is None:
            return False

        conn = self._connect()
        try:
            conn.execute("DELETE FROM habits WHERE id = ?;", (habit.id,))
            conn.commit()
        finally:
            conn.close()

        self.habits.remove(habit)
        return True
