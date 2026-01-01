from shared.database import get_db
from modules.order.service import OrderService

class PaymentService:
    @staticmethod
    def create_payment(order_id):
        order = OrderService.get_order_by_id(order_id)
        if not order:
            raise ValueError('Order not found')
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO payments (order_id, amount) VALUES (?, ?)',
            (order_id, order['total'])
        )
        payment_id = cursor.lastrowid
        
        OrderService.update_order_status(order_id, 'PAID')
        
        conn.commit()
        conn.close()
        
        return {'id': payment_id, 'amount': order['total'], 'status': 'COMPLETED'}
    
    @staticmethod
    def get_all_payments():
        conn = get_db()
        payments = conn.execute('SELECT * FROM payments').fetchall()
        conn.close()
        return [dict(payment) for payment in payments]

