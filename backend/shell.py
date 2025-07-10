from app import app, db
from models import Order
import time, random

def generate_order_no(user_id):
    return f"{int(time.time())}{user_id}{random.randint(1000,9999)}"

with app.app_context():
    orders = Order.query.filter(Order.order_no == None).all()
    for o in orders:
        o.order_no = generate_order_no(o.user_id)
    db.session.commit()
    print(f"补全完成，共补全 {len(orders)} 条订单号。")