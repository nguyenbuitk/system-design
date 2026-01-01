from shared.database import get_db
from modules.product.service import ProductService

class OrderService:
    @staticmethod
    def create_order(user_id, product_id, quantity):
        product = ProductService.get_product_by_id(product_id)
        if not product:
            raise ValueError('Product not found')
        
        total = product['price'] * quantity
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO orders (user_id, product_id, quantity, total) VALUES (?, ?, ?, ?)',
            (user_id, product_id, quantity, total)
        )
        order_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {'id': order_id, 'total': total, 'status': 'PENDING'}
    
    @staticmethod
    def get_all_orders():
        conn = get_db()
        orders = conn.execute('''
            SELECT o.*, u.email, p.name as product_name
            FROM orders o
            JOIN users u ON o.user_id = u.id
            JOIN products p ON o.product_id = p.id
        ''').fetchall()
        conn.close()
        return [dict(order) for order in orders]
    
    @staticmethod
    def get_order_by_id(order_id):
        conn = get_db()
        order = conn.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
        conn.close()
        return dict(order) if order else None
    
    @staticmethod
    def update_order_status(order_id, status):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('UPDATE orders SET status = ? WHERE id = ?', (status, order_id))
        conn.commit()
        conn.close()

