from ast import JoinedStr
from typing import Any
from flask import Flask, render_template_string, request, jsonify, redirect, url_for, render_template
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DB_FILE = 'database/app.db'

def init_db():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE, 
            name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            total REAL,
            status TEXT DEFAULT 'PENDING',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES productsS(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY,
            order_id INTEGER,
            amount REAL,
            status TEXT DEFAULT 'PENDING',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn
    

# =========== User mangement ================
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            'INSERT INTO users (email, name) VALUES (?, ?)',
            (data['email'], data['name'])
        )
        user_id = cursor.lastrowid
        conn.commit()
        print("User created successfully")
        return jsonify({'id': user_id, 'name': data['name'], 'email': data['email']})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already exists'}), 400
    finally:
        conn.close()

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return jsonify([dict[Any, Any](user) for user in users])

# ===== Product ========
@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO products (name, price) VALUES (?, ?)',
        (data['name'], data['price'])
    )
    product_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'id': product_id, 'name': data['name'], 'price': data['price']}), 201

@app.route('/api/products', methods=['GET'])
def get_products():
    conn = get_db()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return jsonify([dict[Any, Any](product) for product in products])

# ====== Order Processing ====
@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json
    print(f"Data: {data}")
    conn = get_db()
    cursor = conn.cursor()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (data['product_id'],)).fetchone()
    print(f"Product: {product}")
    if not product:
        conn.close()
        return jsonify({'error': 'Product not found'}), 404
    total = product['price'] * data['quantity']
    print(f"Total: {total}")
    cursor.execute(
        'INSERT INTO orders (user_id, product_id, quantity, total) VALUES (?, ?, ?, ?)',
        (data['user_id'], data['product_id'], data['quantity'], total)
    )
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return jsonify({'id': order_id, 'total': total, 'status': 'PENDING'}), 201

@app.route('/api/orders', methods=['GET'])
def get_orders():
    conn = get_db()
    orders = conn.execute('''
        SELECT o.*, u.email, p.name as product_name
        FROM orders o
        JOIN users u on o.user_id = u.id
        JOIN products p ON o.product_id = p.id
    ''').fetchall()
    conn.close()
    return jsonify([dict(order) for order in orders])

@app.route('/api/payments', methods=['POST'])
def create_payment():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    
    # Get order
    order = conn.execute('SELECT * FROM orders WHERE id = ?', (data['order_id'],)).fetchone()
    if not order:
        conn.close()
        return jsonify({'error': 'Order not found'}), 404

    # Create payment process
    cursor.execute(
        'INSERT INTO payments (order_id, amount) VALUES (?, ?)',
        (data['order_id'], order['total'])
    )
    payment_id = cursor.lastrowid
    
    # Update order status
    cursor.execute('UPDATE orders SET status = ? WHERE id = ?', ('PAID', data['order_id']))
    conn.commit()
    conn.close()
    
    return jsonify({'id': payment_id, 'amount': order['total'], 'status': 'COMPLETED'}), 201

@app.route('/api/payments', methods=['GET'])
def get_payments():
    conn = get_db()
    payments = conn.execute('SELECT * FROM payments').fetchall()
    conn.close()
    return jsonify([dict(payment) for payment in payments])

@app.route('/')
def index():
    return render_template("index.html")   

if __name__ == '__main__':
    init_db()
    print("\nRunning on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
    
