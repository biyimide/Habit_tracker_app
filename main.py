"""Command-line interface for the habit tracker (input()-based menu loop).

The CLI contains no business logic: every menu option calls one HabitManager
method or one analytics function.
"""
from datetime import datetime

from analytics import analytics
from db.database import init_db
from db.fixtures import seed_database
from models.habit_manager import HabitManager

MENU = """
==============================
      HABIT TRACKER MENU
==============================
1. List all habits
2. Create a new habit
3. Check off a habit
4. List habits by periodicity (daily/weekly)
5. View longest streak overall
6. View longest streak for a specific habit
7. Delete a habit
8. Habits I struggled with most (last 4 weeks)
9. Exit
=============================="""


def list_all(manager: HabitManager) -> None:
    """Menu option 1: show every habit with its periodicity."""
    habits = manager.list_habits()
    print("\nCurrently tracked habits:")
    if not habits:
        print("  No habits found.")
    for habit in habits:
        print("  - {} ({})".format(habit.name, habit.periodicity))


def create(manager: HabitManager) -> None:
    """Menu option 2: create a daily or weekly habit."""
    name = input("Enter habit name: ").strip()
    periodicity = input("Enter periodicity ('daily' or 'weekly'): ").strip()
    try:
        habit = manager.create_habit(name, periodicity)
        print("Habit '{}' ({}) created.".format(habit.name, habit.periodicity))
    except ValueError as error:
        print("Could not create habit: {}".format(error))


def check_off(manager: HabitManager) -> None:
    """Menu option 3: check a habit off right now."""
    name = input("Enter the name of the habit to check off: ").strip()
    if manager.complete_habit(name):
        print("Habit '{}' checked off.".format(name))
    else:
        print("Habit '{}' not found.".format(name))


def list_by_periodicity(manager: HabitManager) -> None:
    """Menu option 4: list only daily or only weekly habits."""
    period = input("Enter periodicity to filter ('daily' or 'weekly'): ").strip()
    habits = analytics.get_habits_by_periodicity(manager.list_habits(), period)
    print("\nHabits with periodicity '{}':".format(period.lower()))
    if not habits:
        print("  No habits found.")
    for habit in habits:
        print("  - {}".format(habit.name))


def longest_overall(manager: HabitManager) -> None:
    """Menu option 5: longest streak across all habits."""
    streak = analytics.get_longest_streak(manager.list_habits())
    print("\nLongest streak across all habits: {} period(s).".format(streak))


def longest_for_habit(manager: HabitManager) -> None:
    """Menu option 6: longest streak of one habit."""
    name = input("Enter the name of the habit: ").strip()
    habit = manager.get_habit(name)
    if habit is None:
        print("Habit '{}' not found.".format(name))
        return
    streak = analytics.get_longest_streak_for_habit(habit)
    unit = "day(s)" if habit.periodicity == "daily" else "week(s)"
    print("\nLongest streak for '{}': {} {}.".format(habit.name, streak, unit))


def delete(manager: HabitManager) -> None:
    """Menu option 7: delete a habit and its completions."""
    name = input("Enter the name of the habit to delete: ").strip()
    if manager.delete_habit(name):
        print("Habit '{}' deleted.".format(name))
    else:
        print("Habit '{}' not found.".format(name))


def struggled(manager: HabitManager) -> None:
    """Menu option 8: rank habits by periods missed in the last 4 weeks."""
    ranking = analytics.get_struggled_habits(manager.list_habits(), datetime.now())
    print("\nMissed periods over the last 4 weeks (most struggled first):")
    if not ranking:
        print("  No habits found.")
    for name, missed in ranking:
        print("  - {}: {} missed".format(name, missed))


ACTIONS = {
    "1": list_all, "2": create, "3": check_off, "4": list_by_periodicity,
    "5": longest_overall, "6": longest_for_habit, "7": delete, "8": struggled,
}


def main() -> None:
    """Initialise the database, seed example data on first run, run the menu."""
    init_db()
    manager = HabitManager()
    if seed_database(manager):
        print("First run: loaded 5 predefined habits with 4 weeks of example data.")

    while True:
        print(MENU)
        choice = input("Choose an option (1-9): ").strip()
        if choice == "9":
            print("\nGoodbye! Keep building great habits!")
            break
        action = ACTIONS.get(choice)
        if action is None:
            print("Invalid choice. Please enter a number between 1 and 9.")
        else:
            action(manager)


if __name__ == "__main__":
    main()
