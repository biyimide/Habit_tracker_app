from datetime import datetime
import functools
from typing import List, Tuple
from models.habit import Habit

def get_all_habits(habits: List[Habit]) -> List[str]:
    """Returns the names of all tracked habits using a list comprehension."""
    return [habit.name for habit in habits]

def get_habits_by_periodicity(habits: List[Habit], periodicity: str) -> List[Habit]:
    """Filters habits matching 'daily' or 'weekly' using filter()."""
    return list(filter(lambda h: h.periodicity.lower() == periodicity.lower(), habits))

def get_longest_streak_for_habit(habit: Habit) -> int:
    """Calculates the longest consecutive run streak for a single habit."""
    if not habit.completions:
        return 0
    
    # Sort completion dates to ensure they are chronological
    sorted_dates = sorted(list({c.date() for c in habit.completions}))
    
    if len(sorted_dates) == 1:
        return 1

    # Reducer logic to count consecutive runs
    def streak_reducer(acc, next_date):
        longest, current, prev_date = acc
        if prev_date is None:
            return (1, 1, next_date)
        
        # Check if the next date is the very next consecutive day
        delta_days = (next_date - prev_date).days
        if delta_days == 1:
            new_current = current + 1
            return (max(longest, new_current), new_current, next_date)
        elif delta_days == 0:
            # Duplicate check-in on the same day doesn't break or grow the streak
            return (longest, current, prev_date)
        else:
            # Streak broken, reset current streak to 1
            return (longest, 1, next_date)

    initial_state = (0, 0, None)
    result = functools.reduce(streak_reducer, sorted_dates, initial_state)
    return result[0]

def get_longest_streak(habits: List[Habit]) -> int:
    """Finds the maximum streak across all tracked habits."""
    if not habits:
        return 0
    return max(map(get_longest_streak_for_habit, habits))