from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from models import User, Category, Product, Order, OrderItem
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint
from db import db
api_bp = Blueprint('api', __name__)

@api_bp.route('/api/seller/login', methods=['POST'])
def seller_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username, role='seller').first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "用户名或密码错误，或非商家账号"}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token, "username": user.username,"role": user.role}), 200

@api_bp.route('/api/seller/products', methods=['POST'])
@jwt_required()
def add_product():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user.role != 'seller':
        return jsonify({"message": "仅商家可添加商品"}), 403
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        price=data['price'],
        stock=data['stock'],
        category_id=data['category_id'],
        description=data.get('description'),
        image_url=data.get('image_url'),
        seller_id=user_id
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "商品添加成功", "product_id": new_product.id}), 201

@api_bp.route('/api/seller/products', methods=['GET'])
@jwt_required()
def get_seller_products():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user.role != 'seller':
        return jsonify({"message": "仅商家可查看商品"}), 403
    products = Product.query.filter_by(seller_id=user_id).all()
    return jsonify([{
        "id": p.id,
        "name": p.name,
        "price": float(p.price),
        "stock": p.stock,
        "category_id": p.category_id,
        "description": p.description,
        "image_url": p.image_url
    } for p in products]), 200

@api_bp.route('/api/seller/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user.role != 'seller':
        return jsonify({"message": "仅商家可编辑商品"}), 403
    product = Product.query.filter_by(id=product_id, seller_id=user_id).first()
    if not product:
        return jsonify({"message": "商品不存在或无权限"}), 404
    data = request.get_json()
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.stock = data.get('stock', product.stock)
    product.category_id = data.get('category_id', product.category_id)
    product.description = data.get('description', product.description)
    product.image_url = data.get('image_url', product.image_url)
    db.session.commit()
    return jsonify({"message": "商品更新成功"}), 200

@api_bp.route('/api/seller/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user.role != 'seller':
        return jsonify({"message": "仅商家可删除商品"}), 403
    product = Product.query.filter_by(id=product_id, seller_id=user_id).first()
    if not product:
        return jsonify({"message": "商品不存在或无权限"}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "商品删除成功"}), 200

@api_bp.route('/api/seller/orders', methods=['GET'])
@jwt_required()
def get_seller_orders():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user.role != 'seller':
        return jsonify({"message": "仅商家可查看订单"}), 403
    orders = Order.query.join(OrderItem).join(Product).filter(Product.seller_id == user_id).all()
    return jsonify([{
        "id": o.id,
        "user_id": o.user_id,
        "total_amount": float(o.total_amount),
        "status": o.status,
        "created_at": o.created_at.isoformat(),
        "items": [{"product_id": i.product_id, "quantity": i.quantity, "unit_price": float(i.unit_price)} for i in o.items]
    } for o in orders]), 200

@api_bp.route('/api/orders', methods=['POST'])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    data = request.get_json()
    items = data.get('items')
    if not items:
        return jsonify({"message": "订单不能为空"}), 400
    total_amount = 0
    for item in items:
        product = Product.query.get(item['product_id'])
        if not product or product.stock < item['quantity']:
            return jsonify({"message": f"商品 {item['product_id']} 不存在或库存不足"}), 400
        total_amount += float(product.price) * item['quantity']
    
    order = Order(user_id=user_id, total_amount=total_amount, status='pending')
    db.session.add(order)
    db.session.flush()
    
    for item in items:
        product = Product.query.get(item['product_id'])
        order_item = OrderItem(
            order_id=order.id,
            product_id=item['product_id'],
            quantity=item['quantity'],
            unit_price=product.price
        )
        product.stock -= item['quantity']
        db.session.add(order_item)
    
    db.session.commit()
    return jsonify({"message": "Order created", "order_id": order.id}), 201

@api_bp.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"message": "用户名或邮箱已存在"}), 400
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password, role='user')
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "用户注册成功"}), 201

@api_bp.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username,role='user').first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "用户名或密码错误"}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token, "username": user.username, "role": user.role}), 200

@api_bp.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        "id": p.id,
        "name": p.name,
        "price": float(p.price),
        "stock": p.stock,
        "category_id": p.category_id,
        "description": p.description,
        "image_url": p.image_url
    } for p in products]), 200

@api_bp.route('/api/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{"id": c.id, "name": c.name, "parent_id": c.parent_id} for c in categories]), 200