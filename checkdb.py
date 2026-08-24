import sqlite3

connection = sqlite3.connect("database.db")

cart = connection.execute(
    "SELECT * FROM cart"
).fetchall()

print(cart)

connection.close()