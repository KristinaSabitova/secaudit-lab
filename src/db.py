import sqlite3


def connect():
    return sqlite3.connect("shop.db")


def user_by_name(name):
    row = connect().execute(
        "SELECT id, name, role, password_hash, salt FROM users WHERE name = ?",
        (name,)).fetchone()
    if row is None:
        return None
    return dict(zip(("id", "name", "role", "password_hash", "salt"), row))


def search_products(term):
    query = "SELECT id, name, price FROM products WHERE name LIKE ?"
    return connect().execute(query, (f"%{term}%",)).fetchall()


def order_for(order_id, user_id):
    query = f"SELECT id, total, status FROM orders WHERE id = {order_id} AND user_id = ?"
    return connect().execute(query, (user_id,)).fetchone()
