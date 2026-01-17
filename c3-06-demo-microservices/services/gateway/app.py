from flask import Flask, render_template, request, jsonify
import requests
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from shared.config import SERVICES

app = Flask(__name__)
PORT = 5000

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    services_status = {}
    print("request.args: ", request.args)
    print("request.method: ", request.method)
    print("request.headers: ", request.headers)

    for service_name, service_url in SERVICES.items():
        try:
            response = requests.get(f"{service_url}/health", timeout=1)
            services_status[service_name] = 'healthy' if response.status_code == 200 else 'unhealthy'
        except:
            services_status[service_name] = 'down'
    return jsonify({'services': services_status})

def forward_request(service_name, path, method='GET', data=None):
    """Forward request to backend service"""
    service_url = SERVICES.get(service_name)
    if not service_url:
        return jsonify({'error': f'Service {service_name} not found'}), 500
    
    url = f"{service_url}{path}"
    try:
        if method == 'GET':
            print("request.args: ", request.args)
            response = requests.get(url, params=request.args, timeout = 5)
        elif method == 'POST':
            response = requests.post(url, json=data or request.json, timeout = 5)
        elif method == 'PUT':
            response = requests.put(url, json=data or request.json, timeout = 5)
        elif method == 'DELETE':
            response = requests.delete(url, timeout = 5)
        else:
            return jsonify({'error': 'Method not supported'}), 405
        return jsonify(response.json()), response.status_code
    
    except requests.RequestException as e:
        return jsonify({'error': f'Service {service_name} unavailable'}), 503
        
# Routing: forward request to backend services
@app.route('/api/users', methods=['GET', 'POST'])
@app.route('/api/users/<int:user_id>', methods=['GET'])
def route_users(user_id=None):
    path = f"/api/users/{user_id}" if user_id else "/api/users"
    return forward_request('user', path, method=request.method)

@app.route('/api/products', methods=['GET', 'POST'])
@app.route('/api/products/<int:product_id>', methods=['GET'])
def route_products(product_id=None):
    path = f"/api/products/{product_id}" if product_id else "/api/products"
    return forward_request('product', path, method=request.method)

@app.route('/api/orders', methods=['GET', 'POST'])
def route_orders():
    return forward_request('order', '/api/orders', method=request.method)

@app.route('/api/orders/user/<int:user_id>', methods=['GET'])
def route_orders_by_user(user_id):
    return forward_request('order', f'/api/orders/user/{user_id}', method=request.method)

@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
def route_order_status(order_id):
    return forward_request('order', f'/api/orders/{order_id}/status', method=request.method)

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def route_order(order_id):
    return forward_request('order', f'/api/orders/{order_id}', method=request.method)

@app.route('/api/payments', methods=['GET', 'POST'])
def route_payments():
    return forward_request('payment', '/api/payments', method=request.method)

@app.route('/api/users/<int:user_id>/details', methods=['GET'])
def get_user_details(user_id):
    """API Composition: User + Orders + Payments"""
    try:
        user_resp = requests.get(f"{SERVICES['user']}/api/users/{user_id}", timeout=5)
        if user_resp.status_code != 200:
            return jsonify({'error': 'User not found'}), 404
        
        orders_resp = requests.get(f"{SERVICES['order']}/api/orders/user/{user_id}", timeout=5)
        orders = orders_resp.json() if orders_resp.status_code == 200 else []
        
        payments_resp = requests.get(f"{SERVICES['payment']}/api/payments", timeout=5)
        payments = payments_resp.json() if payments_resp.status_code == 200 else []
        
        user_orders = [o['id'] for o in orders]
        user_payments = [p for p in payments if p.get('order_id') in user_orders]
        
        return jsonify({
            'user': user_resp.json(),
            'orders': orders,
            'payments': user_payments,
            'summary': {
                'total_orders': len(orders),
                'total_payments': len(user_payments),
                'total_spent': sum(p.get('amount', 0) for p in user_payments)
            }
        })
    except requests.RequestException as e:
        return jsonify({'error': 'Service unavailable'}), 503

@app.route('/api/orders/<int:order_id>/details', methods=['GET'])
def get_order_details(order_id):
    """API Composition: Order + User + Product"""
    try:
        order_resp = requests.get(f"{SERVICES['order']}/api/orders/{order_id}", timeout=5)
        if order_resp.status_code != 200:
            return jsonify({'error': 'Order not found'}), 404
        
        order = order_resp.json()
        user_id = order.get('user_id')
        product_id = order.get('product_id')
        
        user_resp = requests.get(f"{SERVICES['user']}/api/users/{user_id}", timeout=5)
        product_resp = requests.get(f"{SERVICES['product']}/api/products/{product_id}", timeout=5)
        
        return jsonify({
            'order': order,
            'user': user_resp.json() if user_resp.status_code == 200 else None,
            'product': product_resp.json() if product_resp.status_code == 200 else None
        })
    except requests.RequestException as e:
        return jsonify({'error': 'Service unavailable'}), 503



if __name__ == '__main__':
    print(f"\nAPI Gateway running on http://localhost:{PORT}")
    print("\nFeatures:")
    print("  - Routing: Forward requests to backend services")
    print("  - API Composition: Combine data from multiple services")
    print("\nMake sure all services are running:")
    print("  - User Service: http://localhost:5001")
    print("  - Product Service: http://localhost:5002")
    print("  - Order Service: http://localhost:5003")
    print("  - Payment Service: http://localhost:5004")
    app.run(host='0.0.0.0', port=PORT, debug=True)

