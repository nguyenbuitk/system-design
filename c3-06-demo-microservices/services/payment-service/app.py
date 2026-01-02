from flask import Flask, request, jsonify
import sqlite3
import os
import requests
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from shared.config import SERVICES

app = Flask(__name__)
DB_FILE = 'database/payments.db'
PORT = 5004

def init_db():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY,
            order_id INTEGER,
            amount REAL,
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

def get_order_from_service(order_id):
    try:
        response = requests.get(f"{SERVICES['order']}/api/orders/{order_id}", timeout=2)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.RequestException:
        return None

def update_order_status(order_id, status):
    try:
        response = requests.put(
            f"{SERVICES['order']}/api/orders/{order_id}/status",
            json={'status': status},
            timeout=2
        )
        return response.status_code == 200
    except requests.RequestException:
        return False

@app.route('/api/payments', methods=['POST'])
def create_payment():
    data = request.json
    
    order = get_order_from_service(data['order_id'])
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    if order['status'] == 'PAID':
        return jsonify({'error': 'Order already paid'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO payments (order_id, amount) VALUES (?, ?)',
        (data['order_id'], order['total'])
    )
    payment_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    update_order_status(data['order_id'], 'PAID')
    
    return jsonify({'id': payment_id, 'amount': order['total'], 'status': 'COMPLETED'}), 201

@app.route('/api/payments', methods=['GET'])
def get_payments():
    conn = get_db()
    payments = conn.execute('SELECT * FROM payments').fetchall()
    conn.close()
    return jsonify([dict(payment) for payment in payments])

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'payment-service'})

if __name__ == '__main__':
    init_db()
    print(f"\nPayment Service running on http://localhost:{PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=True)

