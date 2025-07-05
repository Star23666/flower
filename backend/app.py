from flask import Flask
from db import db
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# 创建 Flask 应用
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

db.init_app(app)

# 初始化 JWT 和 CORS
jwt = JWTManager(app)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

from api import api_bp # 导入 api.py 以注册路由
app.register_blueprint(api_bp)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 确保表结构同步
    app.run(debug=True)