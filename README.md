# ShopEase - E-Commerce Website

A simple full-stack e-commerce website built with Python, Flask, SQLite, HTML, CSS, and JavaScript.

This project is developed as a portfolio project to demonstrate practical skills in web development, backend programming, database management, authentication, and software development.

## Technologies Used

- Python
- Flask
- SQLite
- HTML5
- CSS3
- JavaScript
- Jinja2

## Features

- User registration and login
- Secure password hashing
- Product listing
- Product search
- Category filtering
- Product details
- Shopping cart
- Cart quantity management
- Checkout
- Order placement
- Order confirmation
- Order history
- Order details
- User-specific cart and order data

## Database

The application uses SQLite for data storage.

The database contains tables for:

- Products
- Users
- Cart
- Orders
- Order Items

## Authentication

Users can create an account and log in to the application.

Passwords are securely hashed before being stored in the database.

User-specific cart and order information is protected so that users only access their own data.

## Project Structure

```text
EcommerceWebsite/
│
├── app.py
├── database.py
├── .gitignore
├── README.md
│
├── static/
│   └── style.css
│
└── templates/
    ├── index.html
    ├── login.html
    ├── register.html
    ├── product_details.html
    ├── cart.html
    ├── checkout.html
    ├── order_confirmation.html
    ├── orders.html
    └── order_details.html
```

## How to Run

### 1. Clone the repository

git clone https://github.com/Maliksameer04/EcommerceWebsite.git

cd EcommerceWebsite

### 2. Create a virtual environment

python -m venv venv

### 3. Activate the virtual environment

For Windows:

venv\Scripts\activate

### 4. Install Flask

pip install flask

### 5. Create the database

python database.py

### 6. Run the application

python app.py

### 7. Open the website

Open this address in your browser:

http://127.0.0.1:5000

## Application Flow

```text
Register / Login
       ↓
Browse Products
       ↓
Search / Filter
       ↓
View Product Details
       ↓
Add to Cart
       ↓
Manage Cart
       ↓
Checkout
       ↓
Place Order
       ↓
Order Confirmation
       ↓
My Orders
       ↓
Order Details
```

## Project Status

Core e-commerce functionality has been implemented and tested locally.

## Author

Malik Sameer