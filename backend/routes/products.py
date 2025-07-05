# from flask import Blueprint, request, jsonify
# from routes.models import db, Product, Category
# from flask_jwt_extended import jwt_required

# products_bp = Blueprint('products', __name__)

# @products_bp.route('/', methods=['GET'])
# def get_products():
#     products = Product.query.all()
#     return jsonify([{
#         'id': p.id,
#         'name': p.name,
#         'price': str(p.price),
#         'stock': p.stock,
#         'category_id': p.category_id,
#         'description': p.description,
#         'image_url': p.image_url
#     } for p in products]), 200

# @products_bp.route('/', methods=['POST'])
# @jwt_required()
# def create_product():
#     data = request.get_json()
#     product = Product(
#         name=data['name'],
#         price=data['price'],
#         stock=data['stock'],
#         category_id=data['category_id'],
#         description=data.get('description'),
#         image_url=data.get('image_url')
#     )
#     db.session.add(product)
#     db.session.commit()
#     return jsonify({'message': 'Product created'}), 201