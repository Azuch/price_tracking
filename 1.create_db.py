# create_db.py

import sqlite3
from datetime import datetime

# Create a connection to the database (or create it if it doesn't exist)
conn = sqlite3.connect('products.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create a table to store product data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Add some dummy product data
products = [
    ('Product 1', 10.99),
    ('Product 2', 20.49),
    ('Product 3', 15.99),
]

cursor.executemany('INSERT INTO products (name, price) VALUES (?, ?)', products)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database created successfully and dummy data added.")

