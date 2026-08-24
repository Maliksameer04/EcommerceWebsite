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
@app.route("/add-to-cart/<int:product_id>")
def add_to_cart(product_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, quantity
        FROM cart
        WHERE user_id = ? AND product_id = ?
        """,
        (user_id, product_id)
    )

    item = cursor.fetchone()

    if item:
        cursor.execute(
            """
            UPDATE cart
            SET quantity = quantity + 1
            WHERE id = ?
            """,
            (item[0],)
        )
    else:
        cursor.execute(
            """
            INSERT INTO cart (user_id, product_id, quantity)
            VALUES (?, ?, 1)
            """,
            (user_id, product_id)
        )

    connection.commit()
    connection.close()

    return redirect(url_for("home"))
@app.route("/cart")
def cart():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row

    cart_items = connection.execute(
        """
        SELECT
            cart.product_id,
            cart.quantity,
            products.name,
            products.price,
            products.image
        FROM cart
        JOIN products
        ON cart.product_id = products.id
        WHERE cart.user_id = ?
        """,
        (user_id,)
    ).fetchall()

    connection.close()

    total = sum(
        item["price"] * item["quantity"]
        for item in cart_items
    )

    return render_template(
        "cart.html",
        cart_items=cart_items,
        total=total
    )
@app.route("/cart/increase/<int:product_id>")
def increase_cart(product_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE cart
        SET quantity = quantity + 1
        WHERE user_id = ? AND product_id = ?
        """,
        (session["user_id"], product_id)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("cart"))
@app.route("/cart/decrease/<int:product_id>")
def decrease_cart(product_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE cart
        SET quantity = quantity - 1
        WHERE user_id = ? AND product_id = ?
        """,
        (session["user_id"], product_id)
    )

    cursor.execute(
        """
        DELETE FROM cart
        WHERE user_id = ? AND product_id = ? AND quantity <= 0
        """,
        (session["user_id"], product_id)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("cart"))
@app.route("/cart/remove/<int:product_id>")
def remove_from_cart(product_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM cart
        WHERE user_id = ? AND product_id = ?
        """,
        (session["user_id"], product_id)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("cart"))

if __name__ == "__main__":
    app.run(debug=True)