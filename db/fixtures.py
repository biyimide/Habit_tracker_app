"""Predefined habits and 4 weeks of example tracking data (the test fixture)."""
from datetime import datetime, timedelta
from typing import List, Optional

from models.habit_manager import HabitManager

# 28 days of example data end yesterday. Offsets are days since the start
# (0 = 27 days ago). A habit is checked off on every offset NOT in "missed".
EXAMPLE_DAYS = 28

PREDEFINED_HABITS = [
    # name,              periodicity, missed offsets (days or weeks)
    ("Drink 2L Water",   "daily",     [6, 13, 20]),   # longest streak: 7
    ("Read 20 Pages",    "daily",     [4, 5, 6, 15]),  # longest streak: 12
    ("Meditate",         "daily",     [8, 17]),        # longest streak: 10
    ("Do Laundry",       "weekly",    [2]),            # longest streak: 2
    ("Grocery Shopping", "weekly",    []),             # longest streak: 4
]

EXPECTED_LONGEST_STREAKS = {
    "Drink 2L Water": 7, "Read 20 Pages": 12, "Meditate": 10,
    "Do Laundry": 2, "Grocery Shopping": 4,
}


def example_completions(periodicity: str, missed: List[int],
                        today: Optional[datetime] = None) -> List[datetime]:
    """Build the 4 weeks of completion timestamps for one predefined habit."""
    today = today or datetime.now()
    start = (today - timedelta(days=EXAMPLE_DAYS)).replace(
        hour=8, minute=0, second=0, microsecond=0)
    if periodicity == "weekly":
        offsets = [7 * week for week in range(EXAMPLE_DAYS // 7)]
    else:
        offsets = list(range(EXAMPLE_DAYS))
    kept = [o for i, o in enumerate(offsets) if i not in missed]
    return [start + timedelta(days=o) for o in kept]


def seed_database(manager: HabitManager,
                  today: Optional[datetime] = None) -> bool:
    """Seed the 5 predefined habits with 4 weeks of data into an empty database.

    Returns:
        True if data was seeded, False if the database already had habits.
    """
    if manager.list_habits():
        return False

    today = today or datetime.now()
    created = (today - timedelta(days=EXAMPLE_DAYS)).replace(
        hour=7, minute=0, second=0, microsecond=0)
    for name, periodicity, missed in PREDEFINED_HABITS:
        manager.create_habit(name, periodicity, created_at=created)
        for moment in example_completions(periodicity, missed, today):
            manager.complete_habit(name, moment)
    return True
