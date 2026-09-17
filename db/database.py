import sqlite3

def init_db(db_path: str = "habit_tracker.db") -> None:
    """Initializes the SQLite database and creates the necessary tables."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # 1. Create the habits table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                periodicity TEXT CHECK(periodicity IN ('daily', 'weekly')) NOT NULL,
                created_at TEXT NOT NULL
            );
        """)
        
        # 2. Create the completions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                completed_at TEXT NOT NULL,
                FOREIGN KEY (habit_id) REFERENCES habits (id) ON DELETE CASCADE
            );
        """)
        
        conn.commit()