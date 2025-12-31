@app.route('/orders', methods=['GET'])
def orders_page():
    """Trang đặt hàng"""
    try:
        # Lấy danh sách sản phẩm
        products_response = requests.get(f'{BUSINESS_SERVICE_URL}/api/products')
        products = products_response.json() if products_response.status_code == 200 else []
        
        # Lấy danh sách orders
        orders_response = requests.get(f'{BUSINESS_SERVICE_URL}/api/orders')
        orders = orders_response.json() if orders_response.status_code == 200 else []
        
        return render_template('orders.html', products=products, orders=orders)
    except requests.exceptions.ConnectionError:
        return render_template('orders.html', products=[], orders=[], error='Business service không khả dụng')

@app.route('/orders', methods=['POST'])
def create_order():
    """Tạo đơn hàng"""
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