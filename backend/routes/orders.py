from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Order, OrderDetail, Product

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/', methods=['POST'])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    data = request.get_json()
    items = data['items']  # List of {product_id, quantity}

    total_amount = 0
    for item in items:
        product = Product.query.get(item['product_id'])
        if not product or product.stock < item['quantity']:
            return jsonify({'message': 'Invalid product or insufficient stock'}), 400
        total_amount += product.price * item['quantity']

    order = Order(user_id=user_id, total_amount=total_amount)
    db.session.add(order)
    db.session.flush()  # Get order ID

    for item in items:
        product = Product.query.get(item['product_id'])
        order_detail = OrderDetail(
            order_id=order.id,
            product_id=product.id,
            quantity=item['quantity'],
            unit_price=product.price
        )
        product.stock -= item['quantity']
        db.session.add(order_detail)

    db.session.commit()
    return jsonify({'message': 'Order created', 'order_id': order.id}), 201