from flask import Blueprint, request, jsonify
from modules.product.service import ProductService

product_bp = Blueprint('product', __name__)

@product_bp.route('/api/products', methods=['POST'])
def create_product():
    data = request.json
    product = ProductService.create_product(data['name'], data['price'])
    return jsonify(product), 201

@product_bp.route('/api/products', methods=['GET'])
def get_products():
    products = ProductService.get_all_products()
    return jsonify(products)

