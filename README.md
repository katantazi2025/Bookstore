# 📚 Online Book Store – Console-Based Python Application

## Overview

The **Online Book Store** is a command-line Python application that simulates a real-world book purchasing system. It allows users to browse books, manage a cart, register as members, and complete orders through a checkout process. The application is powered by a MySQL database and supports both member and admin login features.

This system is designed for educational and prototyping purposes, demonstrating key principles in modular programming, database integration, and basic inventory/order management.

---

## Features

✅ **Member Functionality**
- Register as a new user
- Secure login using email and password
- Browse books by subject
- Search for books by title or author
- Add books to a personal shopping cart
- Checkout: generates an order number and invoice
- Automatically saves order details and clears the cart

🔐 **Admin Functionality**
- Login using database credentials
- Future-ready for inventory management or reports

📦 **Checkout Process**
- Fetches user shipping address from the `members` table
- Saves order data into `orders` and `odetail` tables
- Prints a professional invoice with order and shipping details
- Calculates estimated delivery date

---

## Technologies Used

- **Python 3.x**
- **MySQL** (via `mysql-connector-python`)
- **Terminal-based UI**
- `getpass` for secure password input

---

## Database Schema Overview

Ensure you have the following tables in your MySQL database:

### 📘 `books`
- `isbn` (PK)
- `title`
- `author`
- `subject`
- `price`

### 👤 `members`
- `userid` (PK, auto-increment)
- `fname`, `lname`, `email`, `password`
- `address`, `city`, `zip`, `phone`

### 🛒 `cart`
- `userid`
- `isbn`
- `qty`

### 📄 `orders`
- `ono` (Order Number, PK)
- `userid`
- `created` (timestamp)
- `shipAddress`, `shipCity`, `shipZip`

### 🧾 `odetail`
- `ono` (FK to `orders`)
- `isbn` (FK to `books`)
- `qty`
- `amount`

---

## Installation and Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/online-bookstore.git
   cd online-bookstore

2. Install dependencies
pip install mysql-connector-python

3.Configure database
Create the required tables in your MySQL database.

Update database connection logic in OnlineBookStore (usually in bookstore.py) to match your credentials.

4.Run the application
python menu.py

Usage Guide
🔐 Login Options
Admin Login: Uses MySQL database credentials for authentication.

Member Login: Email and password required (after registration).

🧭 Navigation
Main Menu: Choose to login as member/admin or register as a new user.

Member Menu: After login, browse/search for books, add to cart, and checkout.

🧾 Invoice
Upon checkout, the app will:

Display books in cart with quantities and total prices

Create a new order with a unique order number

Save all order items to the odetail table

Print a full invoice including shipping address and delivery estimate.

online-bookstore/
├── menu.py               # Entry point and menu logic
├── cart.py               # Handles cart operations
├── checkout.py           # Manages checkout, orders, and invoice
├── bookstore.py          # Handles DB connection and authentication
├── memberregister.py     # Handles member login/registration
├── searchbooks.py        # Implements search functionality
├── book.py               # Book browsing logic
├── README.md             # Project documentation

Example Flow
Run python menu.py

Register as a new user or log in as a member

Search or browse books

Add desired books to cart

Proceed to checkout

System prints invoice and clears the cart

Future Improvements
Admin portal for book inventory management

Email confirmation of order

GUI integration using Tkinter or PyQt

REST API or Web Frontend

Author: 
Harrison Katantazi