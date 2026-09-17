from db.database import init_db
from models.habit_manager import HabitManager
from analytics import analytics

def print_menu():
    print("\n==============================")
    print("      HABIT TRACKER MENU      ")
    print("==============================")
    print("1. List all habits")
    print("2. Create a new habit")
    print("3. Check off a habit")
    print("4. List habits by periodicity (Daily/Weekly)")
    print("5. View longest streak overall")
    print("6. View longest streak for a specific habit")
    print("7. Exit")
    print("==============================\n")

def seed_test_fixtures(manager: HabitManager):
    """Seeds 5 predefined habits with sample data if database is brand new."""
    if not manager.habits:
        print("🌱 Seeding default habits and test fixtures...")
        # Create default habits
        manager.create_habit("Drink 2L Water", "daily")
        manager.create_habit("Read 20 Pages", "daily")
        manager.create_habit("Meditate", "daily")
        manager.create_habit("Do Laundry", "weekly")
        manager.create_habit("Grocery Shopping", "weekly")
        
        # Check them off a few times as example data
        for habit in manager.habits:
            manager.complete_habit(habit.name)
        print("✅ Default habits loaded successfully!\n")

def main():
    # Initialize database and manager
    init_db()
    manager = HabitManager()
    
    # Automatically seed test fixtures if empty (as required by project specs)
    seed_test_fixtures(manager)

    while True:
        print_menu()
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            habits = manager.habits
            names = analytics.get_all_habits(habits)
            print("\n📋 Currently Tracked Habits:")
            if not names:
                print("No habits found.")
            for name in names:
                # Find matching habit to show periodicity
                h = next(item for item in habits if item.name == name)
                print(f"- {h.name} ({h.periodicity})")

        elif choice == "2":
            name = input("Enter habit name: ").strip()
            periodicity = input("Enter periodicity ('daily' or 'weekly'): ").strip().lower()
            if periodicity in ["daily", "weekly"]:
                manager.create_habit(name, periodicity)
                print(f"🎉 Habit '{name}' created successfully!")
            else:
                print("❌ Invalid periodicity. Must be 'daily' or 'weekly'.")

        elif choice == "3":
            name = input("Enter the name of the habit to check off: ").strip()
            success = manager.complete_habit(name)
            if success:
                print(f"🔥 Habit '{name}' checked off successfully!")
            else:
                print(f"❌ Habit '{name}' not found.")

        elif choice == "4":
            period = input("Enter periodicity to filter ('daily' or 'weekly'): ").strip().lower()
            filtered = analytics.get_habits_by_periodicity(manager.habits, period)
            print(f"\n📋 Habits with periodicity '{period}':")
            if not filtered:
                print("No habits found.")
            for h in filtered:
                print(f"- {h.name}")

        elif choice == "5":
            max_streak = analytics.get_longest_streak(manager.habits)
            print(f"\n🏆 The longest run streak across all habits is: {max_streak} periods!")

        elif choice == "6":
            name = input("Enter the name of the habit: ").strip()
            habit = next((h for h in manager.habits if h.name.lower() == name.lower()), None)
            if habit:
                streak = analytics.get_longest_streak_for_habit(habit)
                print(f"\n🏆 Longest streak for '{habit.name}': {streak} periods!")
            else:
                print(f"❌ Habit '{name}' not found.")

        elif choice == "7":
            print("\nGoodbye! Keep building great habits! 👋")
            break
        else:
            print("❌ Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()
    