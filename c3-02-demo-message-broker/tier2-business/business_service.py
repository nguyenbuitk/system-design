"""
Tier 2: Business Logic Layer
Chịu trách nhiệm xử lý business rules và validation
Kết nối trực tiếp với database (thực tế hơn)
"""

from typing import Any


from flask import Flask, jsonify, request
import sys
import os
import time

from werkzeug.exceptions import ExpectationFailed

# Add shared folder to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from shared.db import get_db_connection, init_db
from shared.config import DEBUG, ORDER_QUEUE
from shared.queue import send_to_queue
from shared.config import VALIDATING_INVENTORY_TIME, CALCULATING_SHIPPING_TIME, SENDING_CONFIRMATION_EMAIL_TIME, UPDATING_ANALYTICS_TIME

app = Flask(__name__)

def validate_product_data(data):
    """Validate business rules"""
    errors = []
    
    name = data.get('name', '').strip()
    price = data.get('price')
    
    # Business Rule 1: Tên sản phẩm không được rỗng
    if not name:
        errors.append('Tên sản phẩm không được để trống')
    
    # Business Rule 2: Tên sản phẩm phải có ít nhất 3 ký tự
    if len(name) < 3:
        errors.append('Tên sản phẩm phải có ít nhất 3 ký tự')
    
    # Business Rule 3: Giá phải là số dương
    if price is None:
        errors.append('Giá sản phẩm là bắt buộc')
    elif not isinstance(price, (int, float)) or price <= 0:
        errors.append('Giá sản phẩm phải là số dương')
    
    return errors
    
@app.route('/api/products', methods=['GET'])
def get_all_products():
    """Lấy tất cả sản phẩm - query trực tiếp từ database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products ORDER BY created_at DESC')
        products = cursor.fetchall()
        conn.close()
        return jsonify([dict(product) for product in products])
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@app.route('/api/products', methods=['POST'])
def create_product():
    """Tạo sản phẩm mới - validate và lưu vào database"""
    data = request.json
    
    # Validate business rules
    errors = validate_product_data(data)
    if errors:
        return jsonify({'errors': errors}), 400
    
    # Nếu validation pass, lưu vào database
    try:
        name = data['name'].strip()
        price = float(data['price'])
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO products (name, price) VALUES (?, ?)',
            (name, price)
        )
        conn.commit()
        product_id = cursor.lastrowid
        conn.close()
        
        return jsonify({'id': product_id, 'name': name, 'price': price}), 201
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Lấy sản phẩm theo ID - query trực tiếp từ database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        product = cursor.fetchone()
        conn.close()
        
        if product:
            return jsonify(dict(product))
        return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json
    print(data)
    # Validate
    product_id = data.get('product_id')
    customer_name = data.get('customer_name', '').strip()
    customer_email = data.get('customer_email', '').strip()
    quantity = data.get('quantity', 1)
    
    if not product_id or not customer_name or not customer_email:
        return jsonify({'error': 'Missing requried fields'}), 400
    
    try:
        # Get product infor
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        product = cursor.fetchone()
        if not product:
            conn.close()
            return jsonify({'error': 'Product not found'}), 404

        product = dict(product)
        total_price = product['price'] * quantity

        # Save order into database (set status: PENDING) until the worker.py (consumer) handle it
        cursor.execute('''
            INSERT INTO orders (product_id, customer_name, customer_email, quantity, total_price, status)
            VALUES (?, ?, ?, ?, ?, 'PENDING')
        ''', (product_id, customer_name, customer_email, quantity, total_price))
        order_id = cursor.lastrowid

        conn.commit()
        conn.close()
        
        # Send order to queue
        order_data = {
            'order_id': order_id,
            'product_id': product_id,
            'product_name': product['name'],
            'customer_name': customer_name,
            'customer_email': customer_email,
            'quantity': quantity,
            'total_price': total_price
        }
        
        send_to_queue(ORDER_QUEUE, order_data)
        return jsonify({
            'order_id': order_id,
            'status': 'PENDING',
            'message': 'Order received, processing in background'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """Lấy danh sách orders"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT o.*, p.name as product_name 
            FROM orders o 
            JOIN products p ON o.product_id = p.id 
            ORDER BY o.created_at DESC
        ''')
        orders = cursor.fetchall()
        conn.close()
        return jsonify([dict(order) for order in orders])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders/sync', methods=['POST'])
def create_order_sync():
    """
    Tạo đơn hàng đồng bộ - KHÔNG dùng message queue
    Xử lý ngay lập tức, user phải đợi
    """
    data = request.json
    
    # Validate
    product_id = data.get('product_id')
    customer_name = data.get('customer_name', '').strip()
    customer_email = data.get('customer_email', '').strip()
    quantity = data.get('quantity', 1)
    
    if not product_id or not customer_name or not customer_email:
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        # Get product info
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        product = cursor.fetchone()
        if not product:
            conn.close()
            return jsonify({'error': 'Product not found'}), 404

        product = dict(product)
        total_price = product['price'] * quantity

        # Save order into database (status: PROCESSING)
        cursor.execute('''
            INSERT INTO orders (product_id, customer_name, customer_email, quantity, total_price, status)
            VALUES (?, ?, ?, ?, ?, 'PROCESSING')
        ''', (product_id, customer_name, customer_email, quantity, total_price))
        order_id = cursor.lastrowid
        conn.commit()
        
        # Xử lý đồng bộ - BLOCKING (user phải đợi)
        print(f"[SYNC] Processing order #{order_id} synchronously...")
        
        # Simulate các bước xử lý (blocking)
        steps = [
            ('Validating inventory', VALIDATING_INVENTORY_TIME),
            ('Calculating shipping', CALCULATING_SHIPPING_TIME),
            ('Sending confirmation email', SENDING_CONFIRMATION_EMAIL_TIME),
            ('Updating analytics', UPDATING_ANALYTICS_TIME),
        ]
        
        for step_name, step_time in steps:
            print(f"  - {step_name}...")
            time.sleep(step_time)  # BLOCKING!
        
        # Update status thành COMPLETED
        cursor.execute(
            'UPDATE orders SET status = ? WHERE id = ?',
            ('COMPLETED', order_id)
        )
        conn.commit()
        conn.close()
        
        print(f"[SYNC] Order #{order_id} completed")
        
        return jsonify({
            'order_id': order_id,
            'status': 'COMPLETED',
            'message': 'Order processed successfully (synchronous)',
            'processing_time': '~2 seconds'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'healthy', 'tier': 'business-logic'})

if __name__ == '__main__':
    # Khởi tạo database khi start service
    init_db()
    print("Business Logic Layer đang chạy trên http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=DEBUG)

