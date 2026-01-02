from flask import Blueprint, request, jsonify
from modules.order.service import OrderService

order_bp = Blueprint('order', __name__)

@order_bp.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json
    try:
        order = OrderService.create_order(
            data['user_id'],
            data['product_id'],
            data['quantity']
        )
        return jsonify(order), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@order_bp.route('/api/orders', methods=['GET'])
def get_orders():
    orders = OrderService.get_all_orders()
    return jsonify(orders)

