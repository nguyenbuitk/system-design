from flask import Flask, request, jsonify
import sqlite3
import os
import requests
import sys
from flask_cors import CORS
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from shared.config import SERVICES

app = Flask(__name__)
DB_FILE = 'database/orders.db'
PORT = 5003
allow_origins = ['http://localhost:5000']
CORS(app, resources={
    r"/api/*": {
        "origins": allow_origins
    }
})
def init_db():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            total REAL,
            status TEXT DEFAULT 'PENDING',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def get_product_from_service(product_id):
    try:
        response = requests.get(f"{SERVICES['product']}/api/products/{product_id}", timeout=2)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.RequestException:
        return None

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json
    
    product = get_product_from_service(data['product_id'])
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    total = product['price'] * data['quantity']
    
    conn = get_db()
    cursor = conn.cursor()
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
    orders = conn.execute('SELECT * FROM orders').fetchall()
    conn.close()
    
    orders_list = []
    for order in orders:
        order_dict = dict(order)
        try:
            user_response = requests.get(f"{SERVICES['user']}/api/users/{order['user_id']}", timeout=2)
            product_response = requests.get(f"{SERVICES['product']}/api/products/{order['product_id']}", timeout=2)
            
            if user_response.status_code == 200:
                order_dict['user_email'] = user_response.json().get('email', 'N/A')
            if product_response.status_code == 200:
                order_dict['product_name'] = product_response.json().get('name', 'N/A')
        except requests.RequestException:
            order_dict['user_email'] = 'N/A'
            order_dict['product_name'] = 'N/A'
        
        orders_list.append(order_dict)
    
    return jsonify(orders_list)

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    conn = get_db()
    order = conn.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    conn.close()
    if order:
        return jsonify(dict(order))
    return jsonify({'error': 'Order not found'}), 404

@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE orders SET status = ? WHERE id = ?', (data['status'], order_id))
    conn.commit()
    conn.close()
    return jsonify({'id': order_id, 'status': data['status']})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'order-service'})

if __name__ == '__main__':
    init_db()
    print(f"\nOrder Service running on http://localhost:{PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=True)

