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

@app.route('/orders', methods=['GET'])
def orders_page():
    try:
        products_response = requests.get(f'{BUSINESS_SERVICE_URL}/api/products')
        products = products_response.json() if products_response.status_code == 200 else []
        
        orders_response = requests.get(f'{BUSINESS_SERVICE_URL}/api/orders')
        orders = orders_response.json() if orders_response.status_code == 200 else []
        print("product: ", products)
        return render_template('orders.html', products=products, orders=orders)
    except requests.exceptions.ConnectionError:
        return render_template('orders.html', products=[], orders=[], error='Business service không khả dụng')
    
@app.route('/orders', methods=['POST'])
def create_order():
    product_id = request.form.get('product_id')
    customer_name = request.form.get('customer_name', '').strip()
    customer_email = request.form.get('customer_email', '').strip()
    quantity = int(request.form.get('quantity', 1))
    
    if not product_id or not customer_name or not customer_email:
        return redirect(url_for('orders_page'))
    
    try:
        response = requests.post(
            f'{BUSINESS_SERVICE_URL}/api/orders',
            json={
                'product_id': int(product_id),
                'customer_name': customer_name,
                'customer_email': customer_email,
                'quantity': quantity
            }
        )
        
        if response.status_code == 201:
            return redirect(url_for('orders_page'))
        else:
            return redirect(url_for('orders_page'))
    except requests.exceptions.ConnectionError:
        return redirect(url_for('orders_page'))

@app.route('/orders-sync', methods=['GET'])
def orders_sync_page():
    """Trang đặt hàng đồng bộ - KHÔNG dùng message queue"""
    try:
        products_response = requests.get(f'{BUSINESS_SERVICE_URL}/api/products')
        products = products_response.json() if products_response.status_code == 200 else []
        
        orders_response = requests.get(f'{BUSINESS_SERVICE_URL}/api/orders')
        orders = orders_response.json() if orders_response.status_code == 200 else []
        
        return render_template('orders-sync.html', products=products, orders=orders)
    except requests.exceptions.ConnectionError:
        return render_template('orders-sync.html', products=[], orders=[], error='Business service không khả dụng')

@app.route('/orders-sync', methods=['POST'])
def create_order_sync():
    """Tạo đơn hàng đồng bộ"""
    product_id = request.form.get('product_id')
    customer_name = request.form.get('customer_name', '').strip()
    customer_email = request.form.get('customer_email', '').strip()
    quantity = int(request.form.get('quantity', 1))
    
    if not product_id or not customer_name or not customer_email:
        return redirect(url_for('orders_sync_page'))
    
    try:
        # Gọi endpoint sync - sẽ BLOCK và đợi xử lý xong
        response = requests.post(
            f'{BUSINESS_SERVICE_URL}/api/orders/sync',
            json={
                'product_id': int(product_id),
                'customer_name': customer_name,
                'customer_email': customer_email,
                'quantity': quantity
            },
            timeout=10  # Timeout sau 10 giây
        )
        
        if response.status_code == 201:
            return redirect(url_for('orders_sync_page'))
        else:
            return redirect(url_for('orders_sync_page'))
    except requests.exceptions.Timeout:
        return render_template('orders-sync.html', 
                             products=[], 
                             orders=[], 
                             error='Request timeout - xử lý quá lâu!')
    except requests.exceptions.ConnectionError:
        return redirect(url_for('orders_sync_page'))

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

