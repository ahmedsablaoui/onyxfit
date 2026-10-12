import sqlite3

from app.config import DATABASE_PATH


def create_database():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS fitness_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                age INTEGER,
                sex TEXT,
                current_weight_kg REAL,
                height_cm REAL,
                goal_weight_kg REAL,
                daily_budget_tnd REAL,
                allergies TEXT,
                chronic_conditions TEXT,
                habits TEXT,
                meals_per_day INTEGER,
                appetite TEXT,
                training_days_per_week INTEGER,
                sport TEXT,
                sport_goal TEXT,
                experience_level TEXT,
                injuries_limitations TEXT,
                marital_status TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                content TEXT NOT NULL,
                source TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

    print(f"Database initialized: {DATABASE_PATH}")


if __name__ == "__main__":
    create_database()
