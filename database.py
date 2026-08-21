import sqlite3


def create_database():
    connection = sqlite3.connect("database.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            image TEXT
        )
    """)

    connection.commit()
    connection.close()


def add_products():
    connection = sqlite3.connect("database.db")

    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM products")

    count = cursor.fetchone()[0]

    if count == 0:
        products = [
            (
                "Laptop",
                55000,
                "Electronics",
                "Powerful laptop for work and entertainment.",
                "💻"
            ),
            (
                "Smartphone",
                25000,
                "Electronics",
                "Modern smartphone with excellent performance.",
                "📱"
            ),
            (
                "Headphones",
                3000,
                "Audio",
                "Comfortable headphones with clear sound.",
                "🎧"
            ),
            (
                "Keyboard",
                2000,
                "Accessories",
                "Reliable keyboard for everyday use.",
                "⌨️"
            )
        ]

        cursor.executemany("""
            INSERT INTO products
            (name, price, category, description, image)
            VALUES (?, ?, ?, ?, ?)
        """, products)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()
    add_products()

    print("Database created successfully!")