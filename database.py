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
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
""")
    connection.commit()
    connection.close()

def add_products():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    products = [
        ("Laptop", 55000, "Electronics",
         "Powerful laptop for work and entertainment.", "💻"),

        ("Smartphone", 25000, "Electronics",
         "Modern smartphone with excellent performance.", "📱"),

        ("Headphones", 3000, "Audio",
         "Comfortable headphones with clear sound.", "🎧"),

        ("Keyboard", 2000, "Accessories",
         "Reliable keyboard for everyday use.", "⌨️"),

        ("Smart Watch", 5000, "Wearables",
         "Track your activities and stay connected.", "⌚"),

        ("Gaming Mouse", 1500, "Accessories",
         "Responsive mouse designed for gaming.", "🖱️"),

        ("Bluetooth Speaker", 2500, "Audio",
         "Portable speaker with high-quality sound.", "🔊"),

        ("Tablet", 18000, "Electronics",
         "Lightweight tablet for entertainment and productivity.", "📱")
    ]

    for product in products:

        cursor.execute(
            "SELECT id FROM products WHERE name = ?",
            (product[0],)
        )

        if cursor.fetchone() is None:

            cursor.execute("""
                INSERT INTO products
                (name, price, category, description, image)
                VALUES (?, ?, ?, ?, ?)
            """, product)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_database()
    add_products()

    print("Database created successfully!")