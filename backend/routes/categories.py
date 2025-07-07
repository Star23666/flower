# from flask import Blueprint, jsonify
# from routes.models import Category

# categories_bp = Blueprint('categories', __name__)

# @categories_bp.route('/', methods=['GET'])
# def get_categories():
#     categories = Category.query.all()
#     return jsonify([{
#         'id': c.id,
#         'name': c.name,
#         'parent_id': c.parent_id
#     } for c in categories]), 200