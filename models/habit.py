"""Object-oriented core of the habit tracker: the Habit class."""
from datetime import datetime
from typing import List, Optional

VALID_PERIODICITIES = ("daily", "weekly")


class Habit:
    """A clearly defined task that must be completed once per period.

    A Habit only knows about its own state (name, periodicity, creation time
    and completion timestamps). It performs no storage and no analysis; those
    concerns live in HabitManager and the analytics module respectively.

    Attributes:
        id: Database primary key, or None if the habit is not stored yet.
        name: Task specification, e.g. "Meditate".
        periodicity: Either "daily" or "weekly".
        created_at: Timestamp of when the habit was created.
        completions: Timestamps of every check-off, in the order recorded.
    """

    def __init__(self, name: str, periodicity: str,
                 created_at: Optional[datetime] = None,
                 habit_id: Optional[int] = None):
        """Create a habit.

        Args:
            name: Task specification. Must not be empty.
            periodicity: "daily" or "weekly" (case-insensitive).
            created_at: Creation timestamp. Defaults to now.
            habit_id: Database id, if the habit already exists in storage.

        Raises:
            ValueError: If the name is empty or the periodicity is unknown.
        """
        name = (name or "").strip()
        periodicity = (periodicity or "").strip().lower()
        if not name:
            raise ValueError("Habit name must not be empty.")
        if periodicity not in VALID_PERIODICITIES:
            raise ValueError(
                "Periodicity must be one of: " + ", ".join(VALID_PERIODICITIES))

        self.id = habit_id
        self.name = name
        self.periodicity = periodicity
        self.created_at = created_at or datetime.now()
        self.completions: List[datetime] = []

    def complete(self, timestamp: Optional[datetime] = None) -> None:
        """Check the habit off by recording a completion timestamp.

        Args:
            timestamp: When the habit was completed. Defaults to now.
        """
        self.completions.append(timestamp or datetime.now())

    def is_broken_in_period(self, period_start: datetime,
                            period_end: datetime) -> bool:
        """Return True if no completion falls inside the given period.

        Both bounds are inclusive. A period without a single check-off means
        the user broke the habit.
        """
        return not any(period_start <= c <= period_end
                       for c in self.completions)

    def __repr__(self) -> str:
        return "Habit(name={!r}, periodicity={!r}, completions={})".format(
            self.name, self.periodicity, len(self.completions))
