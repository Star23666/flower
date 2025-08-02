from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User, Category,Product, Order, OrderItem,Address,UserFavorite,Like,Comment
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint
from db import db
from werkzeug.utils import secure_filename
import os
from decimal import Decimal

import time
import random

def generate_order_no(user_id):
    return f"{int(time.time())}{user_id}{random.randint(1000,9999)}"

api_bp = Blueprint('api', __name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@jwt_required(optional=True)  # 注册时未登录也能传

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api_bp.route('/api/upload/image', methods=['POST'])
def upload_image():
    img_type = request.args.get('type', 'common')  # 可以传 type=avatar 或 type=product
    sub_folder = 'avatars' if img_type == 'avatar' else 'products'
    upload_folder = os.path.join(UPLOAD_FOLDER, sub_folder)
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        os.makedirs(upload_folder, exist_ok=True)  # 注意这里
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        # 返回带子目录的静态路径
        url = f'/static/uploads/{sub_folder}/{filename}'
        return jsonify({'url': url})
    return jsonify({'error': 'Invalid file type'}), 400


@api_bp.route('/api/seller/login', methods=['POST'])
def seller_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username, role='seller').first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "用户名或密码错误，或非商家账号"}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify({
        "access_token": access_token, 
        "username": user.username,
        "role": user.role}), 200

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
        seller_id=user_id,
        target=data.get('target')
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
        "image_url": p.image_url,
        "status": p.status, 
        "target": p.target # 这里用数据库的真实值
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
    product.status = data.get('status', product.status)
    product.target = data.get('target', product.target)
    db.session.commit()
    return jsonify({"message": "商品更新成功"}), 200

@api_bp.route('/api/seller/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    order_detail = OrderItem.query.filter_by(product_id=product_id).first()
    if order_detail:
        return jsonify({"message": "该商品已有订单，无法删除"}), 400
    if user.role != 'seller':
        return jsonify({"message": "仅商家可删除商品"}), 403
    product = Product.query.filter_by(id=product_id, seller_id=user_id).first()
    if not product:
        return jsonify({"message": "商品不存在或无权限"}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "商品删除成功"}), 200

@api_bp.route('/api/orders', methods=['GET'])
@jwt_required()
def get_orders():
    """
    获取所有订单列表（管理员/商家后台用）
    返回每个订单的基本信息和商品明细
    """
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role == 'seller':
        # 商家：查所有包含自己商品的订单
        orders = (
            Order.query
            .join(OrderItem, Order.id == OrderItem.order_id)
            .join(Product, OrderItem.product_id == Product.id)
            .filter(Product.seller_id == user_id)
            .distinct()
            .order_by(Order.created_at.desc())
            .all()
        )
    else:
        # 买家：只查自己的订单
        orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    return jsonify([
        {
            "id": o.id,
            "user_id": o.user_id,  # 下单用户id
            "total_amount": float(o.total_amount),  # 订单总价
            "pay_method": o.pay_method,  # 支付方式
            "receiver": o.receiver,  # 收货人
            "receiver_phone": o.receiver_phone,
            "receiver_address": o.receiver_address,
            "status": o.status,  # 订单状态
            "created_at": o.created_at.isoformat(),
            "order_no": o.order_no,  # 下单时间
            "remark": o.remark,
            # 商品明细列表
            "items": [
                {
                    "product_id": i.product_id,
                    "product_name": i.product.name if hasattr(i, "product") else "",
                    "quantity": i.quantity,
                    "unit_price": float(i.unit_price),
                    "image_url": i.product.image_url if hasattr(i.product, "image_url") else ""


                } for i in o.items
            ]
        }
        for o in orders
    ]), 200

@api_bp.route('/api/orders/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order_detail(order_id):
    """
    获取单个订单详情（含商品明细）
    """
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"message": "订单不存在"}), 404

    return jsonify({
        "id": order.id,
        "user_id": order.user_id,
        "total_amount": float(order.total_amount),
        "pay_method": order.pay_method,
        "receiver": order.receiver,
        "receiver_phone": order.receiver_phone,
        "receiver_address": order.receiver_address,
        "status": order.status,
        "created_at": order.created_at.isoformat(),
        "remark": order.remark,
        "items": [
            {
                "product_id": i.product_id,
                "product_name": i.product.name if hasattr(i, "product") else "",
                "quantity": i.quantity,
                "unit_price": float(i.unit_price),
                "image_url": i.product.image_url if hasattr(i.product, "image_url") else ""
            } for i in order.items
        ]
    }), 200

@api_bp.route('/api/orders/<int:order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"message": "订单不存在"}), 404
    # 你可以加权限校验（比如只有管理员或卖家能删）
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "订单已删除"}), 200

@api_bp.route('/api/orders/<int:order_id>/ship', methods=['PUT'])
@jwt_required()
def ship_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"message": "订单不存在"}), 404
    if order.status != '已支付':
        return jsonify({"message": "只有已支付订单才能发货"}), 400
    order.status = '已发货'
    db.session.commit()
    return jsonify({"message": "订单已发货"}), 200

@api_bp.route('/api/orders/<int:order_id>/confirm', methods=['POST','OPTIONS'] )
@jwt_required(optional=True) # 让 OPTIONS 不报错，但 POST 还是需要 token。
def confirm_order(order_id):
    if request.method == 'OPTIONS':
        # 预检请求直接返回
        return '', 204
    user_id = get_jwt_identity()
    order = Order.query.get(order_id)
    if not order or order.user_id != user_id:
        return jsonify({"message": "订单不存在"}), 404
    if order.status != '已发货':
        return jsonify({"message": "只有已发货订单才能确认收货"}), 400
    order.status = '已完成'
    db.session.commit()
    return jsonify({"message": "订单已确认收货"}), 200

@api_bp.route('/api/orders/<int:order_id>/refund', methods=['POST'])
@jwt_required()
def apply_refund(order_id):
    user_id = int(get_jwt_identity())
    order = Order.query.get(order_id)
    if not order or order.user_id != user_id:
        return jsonify({'message': '订单不存在或无权限'}), 404

    if order.status == '已支付':
        # 立即退款
        order.status = '已退款'
        # 返还余额
        user = User.query.get(user_id)
        user.balance += order.total_amount
        db.session.commit()
        return jsonify({'message': '退款成功，金额已原路退回'}), 200
    elif order.status == '已发货':
        # 进入审核
        order.status = '退款审核中'
        db.session.commit()
        return jsonify({'message': '退款申请已提交，等待审核'}), 200
    else:
        return jsonify({'message': '当前状态不可退款'}), 400

@api_bp.route('/api/orders/<int:order_id>/refund/approve', methods=['POST', 'OPTIONS'])
@jwt_required()
def approve_refund(order_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    # 仅商家或管理员可操作
    if user.role not in ['seller', 'admin']:
        return jsonify({'message': '无权限'}), 403
    order = Order.query.get(order_id)
    if order.status != '退款审核中':
        return jsonify({'message': '订单状态不正确'}), 400
    order.status = '已退款'
    buyer = User.query.get(order.user_id)
    buyer.balance += order.total_amount
    db.session.commit()
    return jsonify({'message': '退款审核通过，已退款'}), 200

@api_bp.route('/api/orders/<int:order_id>/refund/reject', methods=['POST', 'OPTIONS'])
@jwt_required()
def reject_refund(order_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user.role not in ['seller', 'admin']:
        return jsonify({'message': '无权限'}), 403
    order = Order.query.get(order_id)
    if order.status != '退款审核中':
        return jsonify({'message': '订单状态不正确'}), 400
    order.status = '退款被拒绝'
    db.session.commit()
    return jsonify({'message': '已拒绝退款'}), 200

@api_bp.route('/api/orders', methods=['POST'])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    data = request.get_json()
    items = data.get('items')
    if not items:
        return jsonify({"message": "订单不能为空"}), 400
    
    total_amount = Decimal('0.00')
    for item in items:
        product = Product.query.get(item['product_id'])
        if not product or product.stock < item['quantity']:
            return jsonify({"message": f"商品 {item['product_id']} 不存在或库存不足"}), 400
        total_amount += product.price * Decimal(str(item['quantity']))
    # 余额校验
    if user.balance < total_amount:
        return jsonify({"message": "余额不足"}), 400
    # 扣除余额
    user.balance -= total_amount

    receiver = data.get('receiver')
    receiver_phone = data.get('receiver_phone')
    receiver_address = data.get('receiver_address')
    order = Order(
        user_id=user_id,
        total_amount=total_amount,
        order_no=generate_order_no(user_id),
        receiver=receiver,
        receiver_phone=receiver_phone,
        receiver_address=receiver_address,
        remark = data.get('remark','')
    )
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
    return jsonify({"success":True,"message": "Order created", "order_id": order.id}), 201

@api_bp.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    gender = data.get('gender')   # 新增
    phone = data.get('phone') 
    avatar = data.get('avatar')    # 新增
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"message": "用户名或邮箱已存在"}), 400
    hashed_password = generate_password_hash(password)
    new_user = User(username=username,
    email=email,
    password=hashed_password,
    role='user',
    gender=gender,
    phone=phone,
    avatar=avatar
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "用户注册成功"}), 201

@api_bp.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(
        username=username,
        role='user',
        ).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "用户名或密码错误"}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify({
        "access_token": access_token, 
        "username": user.username, 
        "role": user.role,
        "avatar": user.avatar,
        }), 200

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
        "image_url": p.image_url,
        "target":p.target,
        "status":p.status
    } for p in products]), 200

@api_bp.route('/api/products/<int:product_id>', methods=['GET'])
def get_product_detail(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': '商品不存在'}), 404
    return jsonify({
        "id": product.id,
        "name": product.name,
        "price": float(product.price),
        "stock": product.stock,
        "category_id": product.category_id,
        "description": product.description,
        "image_url": product.image_url,
        "target": product.target,
        # 如有其它字段，继续补充
        "flower_language": getattr(product, "flower_language", None),
        "scene": getattr(product, "scene", None),
        # 点赞数量
        "like_count": Like.query.filter_by(product_id=product.id).count()
    }), 200


@api_bp.route('/api/categories', methods=['GET'])
@jwt_required()
def get_categories():
    categories = Category.query.all()
    return jsonify([{
        "id": c.id,
        "name": c.name,
        "parent_id": c.parent_id
    } for c in categories]), 200
@api_bp.route('/api/categories', methods=['POST'])
@jwt_required()
def add_category():
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({"message": "类别名不能为空"}), 400
    exists = Category.query.filter_by(name=name).first()
    if exists:
        return jsonify({
            "id": exists.id,
            "name": exists.name
        }), 200
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return jsonify({"id": category.id, "name": category.name}), 201

@api_bp.route('/api/categories/<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"message": "分类不存在"}), 404

    # 检查该分类下是否有商品
    product = Product.query.filter_by(category_id=category_id).first()
    if product:
        return jsonify({"message": "该分类下有商品，无法删除"}), 400

    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "分类已删除"}), 200

@api_bp.route('/api/categories/<int:category_id>', methods=['PUT'])
@jwt_required()
def update_category(category_id):
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({"message": "类别名不能为空"}), 400

    category = Category.query.get(category_id)
    if not category:
        return jsonify({"message": "分类不存在"}), 404

    # 检查该分类下是否有商品，禁止编辑
    product = Product.query.filter_by(category_id=category_id).first()
    if product:
        return jsonify({"message": "该分类下有商品，无法编辑"}), 400

    # 检查重名
    exists = Category.query.filter(Category.id != category_id, Category.name == name).first()
    if exists:
        return jsonify({"message": "该名称已存在"}), 400

    category.name = name
    db.session.commit()
    return jsonify({"id": category.id, "name": category.name}), 200
    
@api_bp.route('/api/users', methods=['GET','OPTIONS'])
@jwt_required()
def get_users():
    search = request.args.get('search', '')
    query = User.query
    if search:
        query = query.filter(
            (User.username.like(f'%{search}%')) | (User.email.like(f'%{search}%'))
        )
    users = query.all()
    return jsonify([
        {
            'id': u.id, 
            'username': u.username,
            'email': u.email, 
            'role': u.role,
            'gender': u.gender, 
            'phone': u.phone,
            'avatar': u.avatar,
            'created_at': u.created_at.strftime('%Y-%m-%d %H:%M')
        } for u in users
    ])

@api_bp.route('/api/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "用户不存在"}), 404
    data = request.json
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.gender = data.get('gender', user.gender)
    user.phone = data.get('phone', user.phone)
    user.avatar = data.get('avatar', user.avatar)
    user.password = data.get('password', user.password)
    user.balance = data.get('balance',user.balance)
    db.session.commit()
    return jsonify({"message": "用户信息已更新"}), 200


@api_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    print(f"收到删除用户请求: {user_id}")
    user = User.query.get(user_id)
    if not user:
        print("用户不存在")
        return jsonify({"message": "用户不存在"}), 404

    # 检查该用户是否有订单
    order = Order.query.filter_by(user_id=user_id).first()
    print("user_id:", user_id, "order:", order)
    if order:
        print("该用户有订单，无法删除")
        return jsonify({"message": "该用户有订单，无法删除"}), 400

    try: 
        db.session.delete(user)
        db.session.commit()
        print("删除成功")
        return jsonify({"message": "用户已删除"}), 200
    except Exception as e:
        print("删除失败:", e)
        return jsonify({"message": "删除失败", "error": str(e)}), 500

@api_bp.route('/api/seller/profile', methods=['GET'])
@jwt_required()
def get_seller_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or user.role != 'seller':
        return jsonify({"message": "仅商家可查看资料"}), 403
    return jsonify({
        "id": user.id,
        "username": user.username,
        "phone": user.phone,
        "balance": float(user.balance),
        "created_at": user.created_at.isoformat()
    }), 200

@api_bp.route('/api/seller/profile', methods=['PUT'])
@jwt_required()
def update_seller_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or user.role != 'seller':
        return jsonify({'message': '商家不存在或无权限'}), 404

    data = request.json
    new_username = data.get('username')
    if new_username:
        user.username = new_username
        db.session.commit()
        return jsonify({'message': '用户名已更新'}), 200
    else:
        return jsonify({'message': '用户名不能为空'}), 400

@api_bp.route('/api/seller/password', methods=['PUT'])
@jwt_required()
def change_seller_password():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or user.role != 'seller':
        return jsonify({'message': '商家不存在或无权限'}), 404

    data = request.json
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')

    if not old_password or not new_password or not confirm_password:
        return jsonify({'message': '请填写完整信息'}), 400
    if new_password != confirm_password:
        return jsonify({'message': '两次新密码不一致'}), 400
    if not user.check_password(old_password):
        return jsonify({'message': '旧密码错误'}), 400

    user.set_password(new_password)
    db.session.commit()
    return jsonify({'message': '密码已修改'}), 200

@api_bp.route('/api/user/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    """
    获取当前登录用户的基本信息
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "用户不存在"}), 404
    return jsonify({
        "id": user.id,
        "username": user.username,
        "realname": user.realname if hasattr(user, "realname") else "",
        "gender": user.gender,
        "phone": user.phone,
        "email": user.email,
        "avatar": user.avatar,
        "balance":user.balance
    }), 200

@api_bp.route('/api/user/addresses', methods=['GET'])
@jwt_required()
def get_user_addresses():
    """
    获取当前登录用户的收货地址列表，支持分页
    """
    user_id = get_jwt_identity()
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    query = Address.query.filter_by(user_id=user_id)
    total = query.count()
    addresses = query.offset((page-1)*page_size).limit(page_size).all()
    return jsonify({
        "addresses": [
            {
                "id": addr.id,
                "realname": addr.realname,
                "phone": addr.phone,
                "address": addr.address
            } for addr in addresses
        ],
        "total": total
    }), 200

@api_bp.route('/api/user/addresses', methods=['POST'])
@jwt_required()
def add_user_address():
    user_id = get_jwt_identity()
    data = request.json
    addr = Address(
        user_id=user_id,
        realname=data.get('realname'),
        phone=data.get('phone'),
        address=data.get('address')
    )
    db.session.add(addr)
    db.session.commit()
    return jsonify({"message": "添加成功"}), 201

@api_bp.route('/api/user/addresses/<int:address_id>', methods=['PUT'])
@jwt_required()
def update_user_address(address_id):
    user_id = get_jwt_identity()
    addr = Address.query.filter_by(id=address_id, user_id=user_id).first()
    if not addr:
        return jsonify({"message": "地址不存在"}), 404
    data = request.json
    addr.realname = data.get('realname', addr.realname)
    addr.phone = data.get('phone', addr.phone)
    addr.address = data.get('address', addr.address)
    db.session.commit()
    return jsonify({"message": "更新成功"}), 200

@api_bp.route('/api/user/addresses/<int:address_id>', methods=['DELETE'])
@jwt_required()
def delete_user_address(address_id):
    user_id = get_jwt_identity()
    addr = Address.query.filter_by(id=address_id, user_id=user_id).first()
    if not addr:
        return jsonify({"message": "地址不存在"}), 404
    db.session.delete(addr)
    db.session.commit()
    return jsonify({"message": "删除成功"}), 200


# 添加收藏
@api_bp.route('/api/favorites', methods=['POST' , 'OPTIONS'])
@jwt_required()
def add_favorite():
    if request.method == 'OPTIONS':
        return jsonify({}),200
    user_id = get_jwt_identity()
    data = request.get_json()
    product_id = data.get('product_id')
    
    if not product_id:
        return jsonify({'error': '缺少商品ID'}), 400
    
    # 检查是否已收藏
    if UserFavorite.query.filter_by(user_id=user_id, product_id=product_id).first():
        return jsonify({'error': '该商品已在收藏夹中'}), 400
    
    favorite = UserFavorite(user_id=user_id, product_id=product_id)
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({'message': '收藏成功'}), 201

# 获取用户收藏列表
@api_bp.route('/api/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    try:
        user_id = get_jwt_identity()
        print(f"获取用户 {user_id} 的收藏列表")  # 添加日志
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
    
        # 获取用户收藏的商品（带分页）
        favorites = UserFavorite.query.filter_by(user_id=user_id).order_by(
            UserFavorite.created_at.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)
    
        print(f"找到 {favorites.total} 个收藏项")  # 添加日志

        return jsonify({
            'items': [
                favorite.product.to_dict() if favorite.product else None
                for favorite in favorites.items
            ],
            'total': favorites.total,
            'pages': favorites.pages,
            'current_page': favorites.page
        })
    except Exception as e:
        print(f"获取收藏列表时出错: {str(e)}")  # 添加错误日志
        return jsonify({'error': str(e)}), 500
# 取消收藏
@api_bp.route('/api/favorites/<int:product_id>', methods=['DELETE'])
@jwt_required()
def remove_favorite(product_id):
    user_id = get_jwt_identity()
    
    favorite = UserFavorite.query.filter_by(
        user_id=user_id, 
        product_id=product_id
    ).first_or_404()
    
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({'message': '已取消收藏'})

@api_bp.route('/api/favorites/check', methods=['GET'])
@jwt_required()
def check_favorite():
    user_id = get_jwt_identity()
    product_id = request.args.get('product_id', type=int)
    
    if not product_id:
        return jsonify({'error': '缺少商品ID'}), 400
    
    is_favorited = UserFavorite.query.filter_by(
        user_id=user_id,
        product_id=product_id
    ).first() is not None
    
    return jsonify({'is_favorited': is_favorited})

# 点赞
@api_bp.route('/api/products/<int:product_id>/like', methods=['POST'])
@jwt_required()
def like_product(product_id):
    user_id = get_jwt_identity()
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': '商品不存在'}), 404

    # 检查是否已点赞
    existing = Like.query.filter_by(user_id=user_id, product_id=product_id).first()
    if existing:
        return jsonify({'message': '您已点赞过该商品'}), 400

    like = Like(user_id=user_id, product_id=product_id)
    db.session.add(like)
    db.session.commit()

    # 可选：返回当前点赞数
    like_count = Like.query.filter_by(product_id=product_id).count()
    return jsonify({'message': '点赞成功', 'like_count': like_count}), 200

@api_bp.route('/api/products/<int:product_id>/like', methods=['DELETE'])
@jwt_required()
def unlike_product(product_id):
    user_id = get_jwt_identity()
    like = Like.query.filter_by(user_id=user_id, product_id=product_id).first()
    if not like:
        return jsonify({'message': '您未点赞该商品'}), 400
    db.session.delete(like)
    db.session.commit()
    like_count = Like.query.filter_by(product_id=product_id).count()
    return jsonify({'message': '取消点赞成功', 'like_count': like_count}), 200

@api_bp.route('/api/products/<int:product_id>/like/status', methods=['GET'])
@jwt_required(optional=True)
def like_status(product_id):
    user_id = get_jwt_identity()
    liked = False
    if user_id:
        liked = Like.query.filter_by(user_id=user_id, product_id=product_id).first() is not None
    like_count = Like.query.filter_by(product_id=product_id).count()
    return jsonify({'liked': liked, 'like_count': like_count})

# 评论区
# 获取商品评论
@api_bp.route('/api/products/<int:product_id>/comments', methods=['GET'])
def get_comments(product_id):
    comments = Comment.query.filter_by(product_id=product_id).order_by(Comment.created_at.desc()).all()
    data = [{
        'id': c.id,
        'username': c.user.username,
        'avatar': c.user.avatar,  # 新增头像字段
        'content': c.content,
        'created_at': c.created_at.isoformat()
    } for c in comments]
    return jsonify(data)

# 新增评论
@api_bp.route('/api/products/<int:product_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(product_id):
    user_id = get_jwt_identity()
    content = request.json.get('content')
    print('收到评论:', user_id, product_id, content)
    try:
        comment = Comment(product_id=product_id, user_id=user_id, content=content)
        db.session.add(comment)
        db.session.commit()
        print('评论已保存')
        return jsonify({'message': '评论成功'})
    except Exception as e:
        db.session.rollback()
        print('评论保存异常:', e)
        return jsonify({'message': '评论保存失败', 'error': str(e)}), 500