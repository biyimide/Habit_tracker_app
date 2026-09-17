from datetime import datetime

class Habit:
    def __init__(self, name: str, periodicity: str, created_at=None, habit_id=int):
        """Initializes a new habit object."""
        self.id = habit_id
        self.name = name                        # Task description (e.g., "Meditate")
        self.periodicity = periodicity          # Either "daily" or "weekly"
        self.created_at = created_at or datetime.now()  # When the habit was made
        self.completions = []                   # List to hold check-off timestamps

    def complete(self, timestamp: datetime = None) -> None:
        """Checks off the habit by adding a timestamp to completions."""
        record_time = timestamp if timestamp else datetime.now()
        self.completions.append(record_time)

    def is_broken_in_period(self, period_start: datetime, period_end: datetime) -> bool:
        """Checks if the habit was missed during a specific time interval."""
        # Returns True if NO completion falls between the start and end of the period
        return not any(period_start <= c <= period_end for c in self.completions)