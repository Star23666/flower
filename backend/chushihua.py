# backend/chushihua.py
from werkzeug.security import generate_password_hash
from app import app, db
from models import User, Category, Product, Order, OrderItem
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

with app.app_context():
    logger.info("Starting database initialization...")
    
    # 清空并创建表
    logger.info("Dropping all tables...")
    db.drop_all()
    logger.info("Creating all tables...")
    db.create_all()
    
    # 验证表是否创建
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    logger.info(f"Tables created: {tables}")
    
    # 插入 admin 用户
    if not User.query.filter_by(username='admin').first():
        hashed_password = generate_password_hash('admin')
        admin_user = User(
            username='admin',
            email='admin@example.com',
            password=hashed_password,
            role='seller'
        )
        db.session.add(admin_user)
        logger.info("Added admin user")
    
    # 插入测试用户
    if not User.query.filter_by(username='testuser').first():
        user = User(
            username='testuser',
            email='testuser@example.com',
            password=generate_password_hash('testpass'),
            role='user'
        )
        db.session.add(user)
        logger.info("Added testuser")
    
    # 插入测试分类
    if not Category.query.filter_by(name='Roses').first():
        category = Category(name='Roses', parent_id=None)
        db.session.add(category)
        logger.info("Added Roses category")
    
    # 提交用户和分类
    db.session.commit()
    logger.info("Committed users and categories")
    
    # 插入测试商品
    if not Product.query.filter_by(name='Red Rose').first():
        product = Product(
            name='Red Rose',
            price=5.99,
            stock=100,
            category_id=1,
            description='Beautiful red rose',
            image_url='https://example.com/rose.jpg',
            seller_id=1
        )
        db.session.add(product)
        logger.info("Added Red Rose product")
    
    db.session.commit()
    logger.info("Committed products")
    
    # 插入测试订单
    if not Order.query.filter_by(user_id=2, total_amount=5.99).first():
        order = Order(
            user_id=2,
            total_amount=5.99,
            status='pending'
        )
        db.session.add(order)
        db.session.flush()
        logger.info("Added test order")
        
        # 插入订单项
        order_item = OrderItem(
            order_id=order.id,
            product_id=1,
            quantity=1,
            unit_price=5.99
        )
        db.session.add(order_item)
        logger.info("Added order item")
    
    db.session.commit()
    logger.info("Initialization completed successfully")