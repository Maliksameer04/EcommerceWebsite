from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


def get_products():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row

    products = connection.execute(
        "SELECT * FROM products"
    ).fetchall()

    connection.close()

    return products


@app.route("/")
def home():
    products = get_products()

    return render_template(
        "index.html",
        products=products
    )


if __name__ == "__main__":
    app.run(debug=True)