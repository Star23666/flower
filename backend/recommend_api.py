import pandas as pd
import random
from surprise import Dataset, Reader, KNNBasic
from flask import Blueprint, jsonify, current_app
# 修复导入：从 app.py 导入 db，从 models.py 导入 Product
from models import Product
# 创建推荐功能的蓝图
recommend_bp = Blueprint('recommend', __name__, url_prefix='/api')

# ========== 全局变量：APP启动时初始化 ==========
recommend_model, products_df = None, None

def load_real_products():
    """APP启动时读取鲜花数据（确保在应用上下文中）"""
    try:
        with current_app.app_context():  # 修复：添加应用上下文
            products = Product.query.with_entities(
                Product.id,
                Product.name,
                Product.price,
                Product.image_url
            ).all()
        products_df = pd.DataFrame(products, columns=["product_id", "name", "price", "image_url"])
        print(f"✅ 全局加载 {len(products_df)} 条鲜花数据")
        return products_df
    except Exception as e:
        print(f"❌ 加载鲜花数据失败：{e}")
        return pd.DataFrame()

def generate_behavior_data(products_df):
    """生成模拟行为数据（APP启动时生成一次）"""
    if products_df.empty:
        return pd.DataFrame()
    
    product_ids = products_df["product_id"].tolist()
    user_ids = list(range(1, 51))
    behavior_data = []
    
    for _ in range(500):
        user_id = random.choice(user_ids)
        product_id = random.choice(product_ids)
        behave_type = random.choices(["buy", "favorite"], weights=[0.2, 0.8])[0]
        score = 5 if behave_type == "buy" else 3
        behavior_data.append({
            "user_id": user_id,
            "product_id": product_id,
            "score": score
        })
    
    behavior_df = pd.DataFrame(behavior_data).drop_duplicates(subset=["user_id", "product_id"], keep="last")
    return behavior_df

def train_recommend_model():
    """APP启动时训练一次模型"""
    global products_df
    products_df = load_real_products()
    if products_df.empty:
        return None
    
    behavior_df = generate_behavior_data(products_df)
    if behavior_df.empty:
        return None
    
    reader = Reader(rating_scale=(3, 5))
    dataset = Dataset.load_from_df(behavior_df[["user_id", "product_id", "score"]], reader)
    trainset = dataset.build_full_trainset()
    
    sim_options = {"name": "cosine", "user_based": False}
    model = KNNBasic(sim_options=sim_options)
    model.fit(trainset)
    print("✅ 推荐模型训练完成")
    return model

# ========== 推荐接口 ==========
@recommend_bp.route('/recommend/<int:user_id>', methods=['GET'])
def get_recommend(user_id):
    global recommend_model, products_df
    
    # 初始化模型（APP启动时已训练，这里检查）
    if recommend_model is None:
        recommend_model = train_recommend_model()
        if recommend_model is None:
            return jsonify({"code": 500, "msg": "推荐模型初始化失败"}), 500
    
    # 修复：行为数据在APP启动时已生成，这里复用
    behavior_df = generate_behavior_data(products_df)
    if behavior_df.empty:
        return jsonify({"code": 500, "msg": "行为数据生成失败"}), 500
    
    # 筛选用户未交互的鲜花
    user_interacted = behavior_df[behavior_df["user_id"] == user_id]["product_id"].unique()
    unrated_products = [p for p in products_df["product_id"] if p not in user_interacted]
    
    if not unrated_products:
        return jsonify({"code": 200, "msg": "用户已交互所有鲜花", "data": []})
    
    # 预测评分并排序
    pred_scores = []
    for product_id in unrated_products:
        pred = recommend_model.predict(user_id, product_id)
        buy_count = len(behavior_df[(behavior_df["product_id"] == product_id) & (behavior_df["score"] == 5)])
        total_score = pred.est + (buy_count / 3)
        pred_scores.append((product_id, total_score, pred.est))
    
    pred_scores.sort(key=lambda x: x[1], reverse=True)
    top_products = pred_scores[:5]
    
    # 拼接返回结果
    recommend_list = []
    for p_id, total_score, est_score in top_products:
        p_info = products_df[products_df["product_id"] == p_id].iloc[0]
        recommend_list.append({
            "rank": len(recommend_list) + 1,
            "product_id": int(p_id),
            "name": p_info["name"],
            "price": float(p_info["price"]),
            "image_url": p_info["image_url"] if pd.notna(p_info["image_url"]) else "",
            "pred_score": round(est_score, 2),
            "reason": "购买次数多，个性化推荐优先"
        })
    
    return jsonify({
        "code": 200,
        "msg": "推荐成功",
        "data": recommend_list
    })

# ========== 集成到 app.py ==========
# 在 app.py 中添加：
# from recommend_api import recommend_bp
# app.register_blueprint(recommend_bp)