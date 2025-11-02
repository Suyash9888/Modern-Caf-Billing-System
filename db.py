import sqlite3
from datetime import datetime

def connect_db():
    conn = sqlite3.connect("canteen.db")
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS category (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT UNIQUE NOT NULL
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            category_id INTEGER,
            FOREIGN KEY(category_id) REFERENCES category(category_id)
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS bills (
            bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_amount REAL NOT NULL,
            date TEXT DEFAULT (datetime('now','localtime'))
        )
    ''')

    conn.commit()
    conn.close()


def insert_menu_items():
    conn = sqlite3.connect("canteen.db")
    cur = conn.cursor()

    categories = ['Beverages', 'Snacks', 'Main Course', 'Desserts']
    for cat in categories:
        cur.execute("INSERT OR IGNORE INTO category(category_name) VALUES(?)", (cat,))

    cur.execute("SELECT * FROM category")
    category_map = {row[1]: row[0] for row in cur.fetchall()}

    items = [
        ("Tea", 15, "Beverages"), ("Coffee", 25, "Beverages"),
        ("Cold Coffee", 40, "Beverages"), ("Mango Shake", 50, "Beverages"),
        ("Samosa", 20, "Snacks"), ("Veg Sandwich", 35, "Snacks"),
        ("Burger", 60, "Snacks"), ("Pasta", 80, "Main Course"),
        ("Fried Rice", 90, "Main Course"), ("Chole Bhature", 100, "Main Course"),
        ("Paneer Roll", 75, "Snacks"), ("Gulab Jamun", 25, "Desserts"),
        ("Ice Cream", 30, "Desserts"), ("Brownie", 45, "Desserts")
    ]

    for name, price, cat in items:
        cur.execute('''INSERT OR IGNORE INTO menu(name, price, category_id)
                       VALUES(?, ?, ?)''', (name, price, category_map[cat]))

    conn.commit()
    conn.close()


def get_menu(search_term=None):
    conn = sqlite3.connect("canteen.db")
    cur = conn.cursor()
    if search_term:
        cur.execute('''SELECT m.item_id, m.name, m.price, c.category_name
                       FROM menu m JOIN category c ON m.category_id = c.category_id
                       WHERE m.name LIKE ?''', ('%' + search_term + '%',))
    else:
        cur.execute('''SELECT m.item_id, m.name, m.price, c.category_name
                       FROM menu m JOIN category c ON m.category_id = c.category_id''')
    rows = cur.fetchall()
    conn.close()
    return rows


def save_bill(total_amount):
    conn = sqlite3.connect("canteen.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO bills(total_amount) VALUES(?)", (total_amount,))
    conn.commit()
    conn.close()


def get_total_sales():
    conn = sqlite3.connect("canteen.db")
    cur = conn.cursor()
    cur.execute("SELECT SUM(total_amount) FROM bills")
    result = cur.fetchone()[0]
    conn.close()
    return result if result else 0


def get_all_bills():
    conn = sqlite3.connect("canteen.db")
    cur = conn.cursor()
    cur.execute("SELECT bill_id, total_amount, date FROM bills ORDER BY date DESC")
    rows = cur.fetchall()
    conn.close()
    return rows
