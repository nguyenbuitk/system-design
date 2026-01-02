from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_FILE = 'database/products.db'
PORT = 5002

def init_db():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

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
    return jsonify([dict(product) for product in products])

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn = get_db()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    if product:
        return jsonify(dict(product))
    return jsonify({'error': 'Product not found'}), 404

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'product-service'})

if __name__ == '__main__':
    init_db()
    print(f"\nProduct Service running on http://localhost:{PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=True)

