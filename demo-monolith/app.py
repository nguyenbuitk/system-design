#!/usr/bin/env python3
"""
Monolith Application - Case Study 1: Startup
Tất cả features trong một ứng dụng duy nhất
"""
from flask import Flask, render_template_string, request, jsonify, redirect, url_for
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DB_FILE = 'database/app.db'

def init_db():
    """Khởi tạo database"""
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
            FOREIGN KEY (product_id) REFERENCES products(id)
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
    """Lấy database connection"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# ========== User Management ==========
@app.route('/api/users', methods=['POST'])
def create_user():
    """Tạo user mới"""
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
        return jsonify({'id': user_id, 'email': data['email'], 'name': data['name']}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already exists'}), 400
    finally:
        conn.close()

@app.route('/api/users', methods=['GET'])
def get_users():
    """Lấy danh sách users"""
    conn = get_db()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return jsonify([dict(user) for user in users])

# ========== Product Catalog ==========
@app.route('/api/products', methods=['POST'])
def create_product():
    """Tạo sản phẩm mới"""
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
    """Lấy danh sách sản phẩm"""
    conn = get_db()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return jsonify([dict(product) for product in products])

# ========== Order Processing ==========
@app.route('/api/orders', methods=['POST'])
def create_order():
    """Tạo đơn hàng"""
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    
    # Lấy product
    product = conn.execute('SELECT * FROM products WHERE id = ?', (data['product_id'],)).fetchone()
    if not product:
        conn.close()
        return jsonify({'error': 'Product not found'}), 404
    
    total = product['price'] * data['quantity']
    
    # Tạo order
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
    """Lấy danh sách orders"""
    conn = get_db()
    orders = conn.execute('''
        SELECT o.*, u.email, p.name as product_name 
        FROM orders o
        JOIN users u ON o.user_id = u.id
        JOIN products p ON o.product_id = p.id
    ''').fetchall()
    conn.close()
    return jsonify([dict(order) for order in orders])

# ========== Payment ==========
@app.route('/api/payments', methods=['POST'])
def create_payment():
    """Tạo payment"""
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    
    # Lấy order
    order = conn.execute('SELECT * FROM orders WHERE id = ?', (data['order_id'],)).fetchone()
    if not order:
        conn.close()
        return jsonify({'error': 'Order not found'}), 404
    
    # Tạo payment
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
    """Lấy danh sách payments"""
    conn = get_db()
    payments = conn.execute('SELECT * FROM payments').fetchall()
    conn.close()
    return jsonify([dict(payment) for payment in payments])

# ========== Web UI ==========
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Monolith Demo - Startup</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
        .section { background: #f5f5f5; padding: 20px; margin: 20px 0; border-radius: 8px; }
        h2 { color: #333; }
        input, select { padding: 8px; margin: 5px; width: 200px; }
        button { padding: 8px 15px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #5568d3; }
        .item { padding: 10px; margin: 5px 0; background: white; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>Monolith Application Demo</h1>
    <p><strong>Case Study 1:</strong> Startup - Tất cả features trong một app</p>
    
    <div class="section">
        <h2>1. User Management</h2>
        <form onsubmit="createUser(event)">
            <input type="email" name="email" placeholder="Email" required>
            <input type="text" name="name" placeholder="Name" required>
            <button type="submit">Create User</button>
        </form>
        <div id="users"></div>
    </div>
    
    <div class="section">
        <h2>2. Product Catalog</h2>
        <form onsubmit="createProduct(event)">
            <input type="text" name="name" placeholder="Product Name" required>
            <input type="number" name="price" placeholder="Price" step="0.01" required>
            <button type="submit">Add Product</button>
        </form>
        <div id="products"></div>
    </div>
    
    <div class="section">
        <h2>3. Order Processing</h2>
        <form onsubmit="createOrder(event)">
            <select name="user_id" id="userSelect" required>
                <option value="">Select User</option>
            </select>
            <select name="product_id" id="productSelect" required>
                <option value="">Select Product</option>
            </select>
            <input type="number" name="quantity" placeholder="Quantity" value="1" required>
            <button type="submit">Create Order</button>
        </form>
        <div id="orders"></div>
    </div>
    
    <div class="section">
        <h2>4. Payment</h2>
        <form onsubmit="createPayment(event)">
            <select name="order_id" id="orderSelect" required>
                <option value="">Select Order</option>
            </select>
            <button type="submit">Process Payment</button>
        </form>
        <div id="payments"></div>
    </div>
    
    <div class="section" style="background: #e7f3ff; border-left: 4px solid #2196F3;">
        <h3>Monolith Characteristics:</h3>
        <ul>
            <li>✅ Tất cả features trong một codebase</li>
            <li>✅ Một database cho tất cả</li>
            <li>✅ Giao tiếp trong process (nhanh)</li>
            <li>✅ Deploy một lần</li>
            <li>✅ Đơn giản, dễ develop</li>
        </ul>
    </div>
    
    <script>
        function createUser(e) {
            e.preventDefault();
            fetch('/api/users', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    email: e.target.email.value,
                    name: e.target.name.value
                })
            }).then(() => loadData());
        }
        
        function createProduct(e) {
            e.preventDefault();
            fetch('/api/products', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    name: e.target.name.value,
                    price: parseFloat(e.target.price.value)
                })
            }).then(() => loadData());
        }
        
        function createOrder(e) {
            e.preventDefault();
            fetch('/api/orders', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    user_id: parseInt(e.target.user_id.value),
                    product_id: parseInt(e.target.product_id.value),
                    quantity: parseInt(e.target.quantity.value)
                })
            }).then(() => loadData());
        }
        
        function createPayment(e) {
            e.preventDefault();
            fetch('/api/payments', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    order_id: parseInt(e.target.order_id.value)
                })
            }).then(() => loadData());
        }
        
        function loadData() {
            fetch('/api/users').then(r => r.json()).then(data => {
                document.getElementById('users').innerHTML = data.map(u => 
                    `<div class="item">${u.name} (${u.email})</div>`
                ).join('');
                const select = document.getElementById('userSelect');
                select.innerHTML = '<option value="">Select User</option>' + 
                    data.map(u => `<option value="${u.id}">${u.name}</option>`).join('');
            });
            
            fetch('/api/products').then(r => r.json()).then(data => {
                document.getElementById('products').innerHTML = data.map(p => 
                    `<div class="item">${p.name} - $${p.price}</div>`
                ).join('');
                const select = document.getElementById('productSelect');
                select.innerHTML = '<option value="">Select Product</option>' + 
                    data.map(p => `<option value="${p.id}">${p.name} - $${p.price}</option>`).join('');
            });
            
            fetch('/api/orders').then(r => r.json()).then(data => {
                document.getElementById('orders').innerHTML = data.map(o => 
                    `<div class="item">Order #${o.id}: ${o.product_name} x${o.quantity} = $${o.total} (${o.status})</div>`
                ).join('');
                const select = document.getElementById('orderSelect');
                select.innerHTML = '<option value="">Select Order</option>' + 
                    data.filter(o => o.status === 'PENDING').map(o => 
                        `<option value="${o.id}">Order #${o.id} - $${o.total}</option>`
                    ).join('');
            });
            
            fetch('/api/payments').then(r => r.json()).then(data => {
                document.getElementById('payments').innerHTML = data.map(p => 
                    `<div class="item">Payment #${p.id}: $${p.amount} (${p.status})</div>`
                ).join('');
            });
        }
        
        loadData();
        setInterval(loadData, 2000);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Trang chủ - Web UI"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    """Health check"""
    return jsonify({'status': 'healthy', 'architecture': 'monolith'})

if __name__ == '__main__':
    init_db()
    print("=" * 60)
    print("Monolith Application - Case Study 1: Startup")
    print("=" * 60)
    print("All features in one application:")
    print("  - User Management")
    print("  - Product Catalog")
    print("  - Order Processing")
    print("  - Payment")
    print("\nRunning on http://localhost:5000")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)

