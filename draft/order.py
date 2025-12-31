
@app.route('/api/orders', methods=['POST'])
def create_order():
    """Tạo đơn hàng mới - lưu vào DB và gửi vào queue để xử lý async"""
    data = request.json
    
    # Validate
    product_id = data.get('product_id')
    customer_name = data.get('customer_name', '').strip()
    customer_email = data.get('customer_email', '').strip()
    quantity = data.get('quantity', 1)
    
    if not product_id or not customer_name or not customer_email:
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        # Lấy thông tin sản phẩm
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        product = cursor.fetchone()
        
        if not product:
            conn.close()
            return jsonify({'error': 'Product not found'}), 404
        
        product = dict(product)
        total_price = product['price'] * quantity
        
        # Lưu order vào database (status: PENDING)
        cursor.execute('''
            INSERT INTO orders (product_id, customer_name, customer_email, quantity, total_price, status)
            VALUES (?, ?, ?, ?, ?, 'PENDING')
        ''', (product_id, customer_name, customer_email, quantity, total_price))
        
        order_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Gửi order vào queue để xử lý async
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
