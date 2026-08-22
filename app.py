from flask import Flask, render_template, request, redirect, url_for,session
import sqlite3

app = Flask(__name__)
app.secret_key = "shopease-secret-key"

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

    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()

    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row

    query = "SELECT * FROM products WHERE 1=1"
    parameters = []

    if search:
        query += " AND (name LIKE ? OR category LIKE ?)"
        parameters.append(f"%{search}%")
        parameters.append(f"%{search}%")

    if category:
        query += " AND category = ?"
        parameters.append(category)

    products = connection.execute(
        query,
        parameters
    ).fetchall()

    connection.close()

    return render_template(
        "index.html",
        products=products,
        search=search,
        category=category
    )

@app.route("/product/<int:product_id>")
def product_details(product_id):

    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row

    product = connection.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    ).fetchone()

    connection.close()

    if product is None:
        return "Product not found.", 404

    return render_template(
        "product_details.html",
        product=product
    )

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        connection = sqlite3.connect("database.db")

        try:
            connection.execute(
                """
                INSERT INTO users (name, email, password)
                VALUES (?, ?, ?)
                """,
                (name, email, password)
            )

            connection.commit()

        except sqlite3.IntegrityError:
            connection.close()

            return "Email already registered."

        connection.close()

        return redirect(url_for("home"))

    return render_template("register.html")
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = sqlite3.connect("database.db")
        connection.row_factory = sqlite3.Row

        user = connection.execute(
            """
            SELECT * FROM users
            WHERE email = ? AND password = ?
            """,
            (email, password)
        ).fetchone()

        connection.close()

        if user:
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]

            return redirect(url_for("home"))

        return "Invalid email or password."

    return render_template("login.html")
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)