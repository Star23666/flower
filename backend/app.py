from flask import Flask
from db import db
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta
import os
from dotenv import load_dotenv
from flask import send_from_directory
from api import api_bp # 导入 api.py 以注册路由


# 添加推荐蓝图导入
from recommend_api import recommend_bp

# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

load_dotenv()

# 1. BASE_DIR 表示项目的根目录（flask-shop）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 2. static_folder 表示项目根目录下的 static 文件夹的绝对路径
static_folder = os.path.join(BASE_DIR, 'static')
# 创建 Flask 应用，并指定 static_folder 为项目根目录下的 static 文件夹
# 这样无论你在哪里启动 Flask，/static/ 路由都会指向根目录的 static 文件夹
app = Flask(__name__, static_folder=static_folder)

@app.route('/static/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(static_folder, 'uploads'), filename)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

db.init_app(app)

# 初始化 JWT 和 CORS
jwt = JWTManager(app)
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": ["http://localhost:8080", "http://127.0.0.1:8080"],
            "supports_credentials": True,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type", "Authorization"]
        }
    }
)


app.register_blueprint(api_bp)

# 添加推荐蓝图注册
app.register_blueprint(recommend_bp)
print("Registered blueprints:", app.blueprints)
print("Routes:", [str(rule) for rule in app.url_map.iter_rules() if '/api/recommend' in str(rule)])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 确保表结构同步
    app.run(debug=True)