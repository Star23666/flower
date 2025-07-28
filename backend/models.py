from db import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)
    password = db.Column(db.String(512), nullable=False)
    role = db.Column(db.String(20), default='user')
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    avatar = db.Column(db.String(256))
    balance = db.Column(db.Numeric(10, 2), default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    def set_password(self, raw_password):
        """
        设置用户密码（加密后存储到数据库）
        :param raw_password: 明文密码
        """
        self.password = generate_password_hash(raw_password)  # 使用 werkzeug 提供的加密方法

    def check_password(self, raw_password):
        """
        校验用户输入的密码是否正确
        :param raw_password: 用户输入的明文密码
        :return: True 表示密码正确，False 表示密码错误
        """
        return check_password_hash(self.password, raw_password)  # 对比加密后的密码
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(10), default='active')  # 'active' 上架, 'inactive' 下架
    target = db.Column(db.String(100))  # 适用对象字段，如“恋人”、“朋友”、“长辈”等

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default='已支付')
    created_at = db.Column(db.DateTime, default=db.func.now())
    items = db.relationship('OrderItem', backref='order', cascade="all, delete-orphan", passive_deletes=True)

    pay_method = db.Column(db.String(20), default='现金支付')  # 仅现金 
    receiver = db.Column(db.String(50))
    receiver_phone = db.Column(db.String(200))
    receiver_address = db.Column(db.String(255))

    order_no = db.Column(db.String(32), unique=True, nullable=False, index=True)

    remark = db.Column(db.String(255), nullable=True)


class OrderItem(db.Model):
    __tablename__ = 'order_details'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship('Product', backref='order_items')
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)

class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    realname = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))