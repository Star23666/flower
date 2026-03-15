import pandas as pd
import random
from surprise import Dataset, Reader, KNNBasic
from flask import Blueprint, jsonify, current_app
from models import Product

recommend_bp = Blueprint('recommend', __name__, url_prefix='/api')

# ========== 全局变量 ==========
recommend_model = None
products_df = None
global_behavior_df = None  # <--- 新增：存储全局行为数据

def load_real_products():
    """APP启动时读取鲜花数据"""
    try:
        with current_app.app_context():
            products = Product.query.with_entities(
                Product.id,
                Product.name,
                Product.price,
                Product.image_url
            ).all()
        # 必须给 columns 赋值，否则 DataFrame 空的时候会出错
        if not products:
             return pd.DataFrame(columns=["product_id", "name", "price", "image_url"])
             
        df = pd.DataFrame(products, columns=["product_id", "name", "price", "image_url"])
        print(f"✅ 全局加载 {len(df)} 条鲜花数据")
        return df
    except Exception as e:
        print(f"❌ 加载鲜花数据失败：{e}")
        return pd.DataFrame(columns=["product_id", "name", "price", "image_url"])

def generate_behavior_data_internal(p_df):
    """(内部函数) 生成模拟行为数据"""
    if p_df is None or p_df.empty:
        return pd.DataFrame()
    
    product_ids = p_df["product_id"].tolist()
    # 模拟 50 个用户
    user_ids = list(range(1, 51))
    behavior_data = []
    
    # 增加数据量到 1000 条，让关联更紧密一点
    for _ in range(1000):
        u_id = random.choice(user_ids)
        p_id = random.choice(product_ids)
        # 80%也是买，增加热度差异
        behave_type = random.choices(["buy", "view"], weights=[0.3, 0.7])[0]
        score = 5 if behave_type == "buy" else 3
        behavior_data.append({
            "user_id": u_id,
            "product_id": p_id,
            "score": score
        })
    
    # 去重，保留最后一次操作
    df = pd.DataFrame(behavior_data)
    df = df.drop_duplicates(subset=["user_id", "product_id"], keep="last")
    return df

def init_recommend_system():
    """初始化推荐系统（加载数据+训练模型）"""
    global recommend_model, products_df, global_behavior_df
    
    print("🔄 正在初始化推荐系统...")
    products_df = load_real_products()
    if products_df.empty:
        print("⚠️ 鲜花数据为空，跳过训练")
        return
    
    global_behavior_df = generate_behavior_data_internal(products_df)
    if global_behavior_df.empty:
        print("⚠️ 行为数据生成失败")
        return
        
    reader = Reader(rating_scale=(3, 5))
    dataset = Dataset.load_from_df(global_behavior_df[["user_id", "product_id", "score"]], reader)
    trainset = dataset.build_full_trainset()
    
    # 使用余弦相似度
    sim_options = {"name": "cosine", "user_based": False}
    model = KNNBasic(sim_options=sim_options)
    model.fit(trainset)
    recommend_model = model
    print("✅ 推荐模型训练完成！")

# ========== 推荐接口 ==========
@recommend_bp.route('/recommend/<int:user_id>', methods=['GET'])
def get_recommend(user_id):
    global recommend_model, products_df, global_behavior_df
    
    # 懒加载：如果请求时还没初始化，尝试初始化
    if recommend_model is None:
        init_recommend_system()
        if recommend_model is None:
             return jsonify({"code": 500, "msg": "推荐系统未就绪", "data": []})

    # 使用全局行为数据
    behavior_df = global_behavior_df
    
    # 1. 找出用户已交互过的商品
    user_interacted = []
    if not behavior_df.empty:
        user_interacted = behavior_df[behavior_df["user_id"] == user_id]["product_id"].unique()
    
    # 2. 找出未交互的商品作为候选集
    # (如果是新用户，interacted 为空，则所有商品都是候选)
    all_pids = products_df["product_id"].tolist()
    candidate_pids = [p for p in all_pids if p not in user_interacted]
    
    # 如果都交互过了，就从所有的里面推
    if not candidate_pids:
        candidate_pids = all_pids
    
    # 3. 预测评分
    pred_scores = []
    for pid in candidate_pids:
        # 模型预测分 (协同过滤)
        pred = recommend_model.predict(user_id, pid)
        est_score = pred.est
        
        # 加上热度分 (BuyCount / 10) 简单的加权
        # 避免冷门商品因为偶然高分排太前
        buy_count = 0
        if not behavior_df.empty:
            buy_count = len(behavior_df[(behavior_df["product_id"] == pid) & (behavior_df["score"] == 5)])
            
        final_score = est_score + (buy_count * 0.1) 
        pred_scores.append({
            "pid": pid,
            "final_score": final_score,
            "est": est_score,
            "hot": buy_count
        })
    
    # 4. 排序取 Top 8
    # 增加一个随机因子，打破默认排序（仅用于演示效果，生产环境可去掉）
    for item in pred_scores:
        # 给分数加一点点微小的随机扰动，防止分数一样时按 ID 排序
        # 调大这个数值(0.5)，强制打乱 ID 1,2,3 的默认顺序
        item["final_score"] += random.uniform(0, 0.5)

    # 打印前几名的分以便调试（请留意后端控制台输出）
    pred_scores.sort(key=lambda x: x["final_score"], reverse=True)
    top_items = pred_scores[:8]
    print(f"User {user_id} Top Scores:", [round(x['final_score'], 2) for x in top_items[:3]])
    
    # 5. 组装数据
    result_list = []
    for item in top_items:
        pid = item["pid"]
        # 从 products_df 找详细信息
        row = products_df[products_df["product_id"] == pid].iloc[0]
        
        result_list.append({
            "rank": len(result_list) + 1,
            "product_id": int(pid),
            "name": row["name"],
            "price": float(row["price"]),
            "image_url": row["image_url"] if pd.notna(row["image_url"]) else "",
            "pred_score": round(item["final_score"], 2),
            "reason": f"热度:{item['hot']} 预测:{round(item['est'],1)}"
        })
    
    return jsonify({
        "code": 200,
        "msg": "success",
        "data": result_list
    })