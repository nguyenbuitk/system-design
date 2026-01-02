"""
Tier 1: Presentation Layer
Chịu trách nhiệm hiển thị UI và nhận input từ user
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
import sys
import os

# Add shared folder to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from shared.config import BUSINESS_SERVICE_URL, DEBUG

print("BUSINESS_SERVICE_URL: ", BUSINESS_SERVICE_URL)
app = Flask(__name__)

@app.route('/')
def index():
    """Trang chủ - hiển thị danh sách sản phẩm"""
    try:
        response = requests.get(f'{BUSINESS_SERVICE_URL}/api/products')
        products = response.json() if response.status_code == 200 else []
        return render_template('index.html', products=products)
    except requests.exceptions.ConnectionError:
        return render_template('index.html', products=[], error='Business service không khả dụng')

@app.route('/products', methods=['POST'])
def create_product():
    """Tạo sản phẩm mới - gọi Business Layer"""
    name = request.form.get('name')
    price = request.form.get('price')
    
    try:
        price_float = float(price)
        response = requests.post(
            f'{BUSINESS_SERVICE_URL}/api/products',
            json={'name': name, 'price': price_float}
        )
        
        if response.status_code == 201:
            return redirect(url_for('index'))
        else:
            error_data = response.json()
            return render_template('index.html', 
                                 products=[], 
                                 error=error_data.get('errors', ['Có lỗi xảy ra']))
    except ValueError:
        return render_template('index.html', 
                             products=[], 
                             error=['Giá sản phẩm phải là số'])
    except requests.exceptions.ConnectionError:
        return render_template('index.html', 
                             products=[], 
                             error=['Business service không khả dụng'])

@app.route('/api/products', methods=['GET'])
def api_get_products():
    """API endpoint - proxy đến Business Layer"""
    try:
        response = requests.get(f'{BUSINESS_SERVICE_URL}/api/products')
        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Service không khả dụng'}), 503

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'healthy', 'tier': 'presentation'})

if __name__ == '__main__':
    print("Presentation Layer đang chạy trên http://localhost:5000")
    print("Kết nối với Business Layer tại:", BUSINESS_SERVICE_URL)
    app.run(host='0.0.0.0', port=5000, debug=DEBUG)

