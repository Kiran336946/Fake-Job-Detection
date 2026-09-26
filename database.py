import sqlite3


DATABASE = "fake_job_detection.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)

    # Allows us to access columns by name
    connection.row_factory = sqlite3.Row

    return connection


def create_tables():

    connection = get_db_connection()

    cursor = connection.cursor()

    # ============================================
    # USERS TABLE
    # ============================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # ============================================
    # ANALYSES TABLE
    # ============================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            job_text TEXT NOT NULL,
            prediction TEXT NOT NULL,
            risk_percentage REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
            REFERENCES users(id)
        )
    """)

    connection.commit()

    connection.close()


if __name__ == "__main__":
    create_tables()

    print("Database created successfully!")
    print("Tables created:")
    print("- users")
    print("- analyses")