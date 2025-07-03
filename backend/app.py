from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from routes.auth import auth_bp
from routes.products import products_bp
from routes.orders import orders_bp
from routes.categories import categories_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    JWTManager(app)
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(orders_bp, url_prefix='/api/orders')
    app.register_blueprint(categories_bp, url_prefix='/api/categories')

    with app.app_context():
        db.create_all()  # Create tables if not exist
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True,host='0.0.0.0')