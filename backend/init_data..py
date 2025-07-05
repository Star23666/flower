# backend/init_data.py
import psycopg2
from werkzeug.security import generate_password_hash
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 数据库连接参数（替换为你的凭据）
db_params = {
    'dbname': 'flower_shop_new',
    'user': 'postgres',
    'password': 'yang2002',
    'host': 'localhost',
    'port': '5432'
}

try:
    # 连接数据库
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    logger.info("Connected to database")

    # 插入 admin 用户
    admin_password = generate_password_hash('admin')
    cur.execute("""
        INSERT INTO users (username, email, password, role)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (username) DO NOTHING
        RETURNING id;
    """, ('admin', 'admin@example.com', admin_password, 'seller'))
    admin_id = cur.fetchone()[0] if cur.rowcount > 0 else 1
    logger.info("Inserted admin user")

    # 插入 testuser 用户
    testuser_password = generate_password_hash('testpass')
    cur.execute("""
        INSERT INTO users (username, email, password, role)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (username) DO NOTHING
        RETURNING id;
    """, ('testuser', 'testuser@example.com', testuser_password, 'user'))
    testuser_id = cur.fetchone()[0] if cur.rowcount > 0 else 2
    logger.info("Inserted testuser")

    # 插入分类
    cur.execute("""
        INSERT INTO categories (name, parent_id)
        VALUES (%s, %s)
        ON CONFLICT (name) DO NOTHING
        RETURNING id;
    """, ('Roses', None))
    category_id = cur.fetchone()[0] if cur.rowcount > 0 else 1
    logger.info("Inserted Roses category")

    # 插入商品
    cur.execute("""
        INSERT INTO products (name, price, stock, category_id, description, image_url, seller_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (name) DO NOTHING
        RETURNING id;
    """, ('Red Rose', 5.99, 100, category_id, 'Beautiful red rose', 'https://example.com/rose.jpg', admin_id))
    product_id = cur.fetchone()[0] if cur.rowcount > 0 else 1
    logger.info("Inserted Red Rose product")

    # 插入订单
    cur.execute("""
        INSERT INTO orders (user_id, total_amount, status)
        VALUES (%s, %s, %s)
        RETURNING id;
    """, (testuser_id, 5.99, 'pending'))
    order_id = cur.fetchone()[0]
    logger.info("Inserted test order")

    # 插入订单项
    cur.execute("""
        INSERT INTO order_details (order_id, product_id, quantity, unit_price)
        VALUES (%s, %s, %s, %s);
    """, (order_id, product_id, 1, 5.99))
    logger.info("Inserted order item")

    # 提交事务
    conn.commit()
    logger.info("Initialization completed successfully")

except Exception as e:
    logger.error(f"Error during initialization: {e}")
    conn.rollback()

finally:
    cur.close()
    conn.close()
    logger.info("Database connection closed")