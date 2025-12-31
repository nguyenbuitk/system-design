"""
Tier 2: Business Logic Layer
Chịu trách nhiệm xử lý business rules và validation
Kết nối trực tiếp với database (thực tế hơn)
"""

from flask import Flask, jsonify, request
import sys
import os

# Add shared folder to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from shared.db import get_db_connection, init_db
from shared.config import DEBUG

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

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'healthy', 'tier': 'business-logic'})

if __name__ == '__main__':
    # Khởi tạo database khi start service
    init_db()
    print("🚀 Business Logic Layer đang chạy trên http://localhost:5001")
    print("💾 Kết nối trực tiếp với database:", os.path.join(os.path.dirname(__file__), '..', 'database', 'products.db'))
    app.run(host='0.0.0.0', port=5001, debug=DEBUG)

