from flask import Blueprint, request, jsonify
from modules.payment.service import PaymentService

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/api/payments', methods=['POST'])
def create_payment():
    data = request.json
    try:
        payment = PaymentService.create_payment(data['order_id'])
        return jsonify(payment), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@payment_bp.route('/api/payments', methods=['GET'])
def get_payments():
    payments = PaymentService.get_all_payments()
    return jsonify(payments)

