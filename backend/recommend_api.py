import pandas as pd
from surprise import Dataset, Reader, KNNBasic
from flask import Blueprint, jsonify, current_app
from models import Product, Order, OrderItem, UserFavorite, Like
from db import db
import random

recommend_bp = Blueprint('recommend', __name__, url_prefix='/api')

# ========== 全局变量 ==========
recommend_model = None
products_df = None
global_behavior_df = None

def load_all_products():
    """APP启动时读取所有商品信息（用于查详情）"""
    try:
        # 在应用上下文中查询
        # 注意：这里只取需要的字段
        products = Product.query.with_entities(
            Product.id,
            Product.name,
            Product.price,
            Product.image_url
        ).all()
        
        if not products:
             return pd.DataFrame(columns=["product_id", "name", "price", "image_url"])
             
        # 转成 DataFrame 方便后续查
        data = [{"product_id": p.id, "name": p.name, "price": float(p.price), "image_url": p.image_url} for p in products]
        df = pd.DataFrame(data)
        print(f"✅ 全局加载 {len(df)} 条商品数据")
        return df
    except Exception as e:
        print(f"❌ 加载商品数据失败：{e}")
        return pd.DataFrame()

def generate_behavior_data():
    """从数据库读取真实用户交互数据（根据图片逻辑：按行为累加权重分）"""
    behavior_dict = {} # 格式: { (user_id, product_id): total_score }
    
    try:
        # 图片规则 3: 下过单该商品权重 +3 (你代码里对应购买)
        orders = db.session.query(Order.user_id, OrderItem.product_id)\
            .join(OrderItem, Order.id == OrderItem.order_id).all()
        for uid, pid in orders:
            key = (uid, pid)
            behavior_dict[key] = behavior_dict.get(key, 0) + 3.0

        # 图片规则 1: 收藏权重 +1
        favorites = UserFavorite.query.with_entities(UserFavorite.user_id, UserFavorite.product_id).all()
        for uid, pid in favorites:
            key = (uid, pid)
            behavior_dict[key] = behavior_dict.get(key, 0) + 1.0

        # 图片规则 2 点赞 +2
        likes = Like.query.with_entities(Like.user_id, Like.product_id).all()
        for uid, pid in likes:
            key = (uid, pid)
            behavior_dict[key] = behavior_dict.get(key, 0) + 2.0

        # 图片规则 4: 评论该商品权重 +2 
        try:
            from models import Comment 
            comments = db.session.query(Comment.user_id, Comment.product_id).all()
            for uid, pid in comments:
                key = (uid, pid)
                behavior_dict[key] = behavior_dict.get(key, 0) + 2.0
        except Exception:
            # 如果没有 Comment 模型，暂且忽略
            pass
            
    except Exception as e:
        print(f"⚠️ 读取真实交互数据失败: {e}")

    # 将字典转为 DataFrame
    if not behavior_dict:
        return pd.DataFrame()

    behavior_list = [{"user_id": k[0], "product_id": k[1], "score": v} for k, v in behavior_dict.items()]
    df = pd.DataFrame(behavior_list)
    
    print(f"✅ 生成规则加权数据: {len(df)} 条交互记录")
    return df

def train_model():
    """训练 User-Based 协同过滤模型"""
    global recommend_model, products_df, global_behavior_df
    
    products_df = load_all_products()
    global_behavior_df = generate_behavior_data()
    
    if not global_behavior_df.empty:
        print(f"📊 当前训练数据:\n{global_behavior_df}")

    # 数据太少无法训练出相似度（比如少于1个用户或1条记录）
    if global_behavior_df.empty or len(global_behavior_df) < 1:
        recommend_model = None
        print("⚠️ 数据不足，跳过模型训练，将使用保底推荐策略")
        return

    # Surprise 库标准流程
    # 根据最新的权重累加规则：最低1分(仅收藏)，最高8分(收藏1+点赞2+评论2+购买3)
    reader = Reader(rating_scale=(1, 8))
    dataset = Dataset.load_from_df(global_behavior_df[["user_id", "product_id", "score"]], reader)
    trainset = dataset.build_full_trainset()
    
    # 使用余弦相似度 + User-Based (基于用户找相似用户)
    sim_options = {
        "name": "cosine",
        "user_based": True,  # True=找相似的人, False=找相似的物品
        "min_support": 1  # 至少有1个共同评分才计算相似度，减少稀疏性影响   
    }
    model = KNNBasic(k=40,min_k=1,sim_options=sim_options, verbose=False)
    model.fit(trainset)
    
    recommend_model = model
    print("✅ 协同过滤模型训练完成！")

# === 核心推荐接口 ===
@recommend_bp.route('/recommend/<int:user_id>', methods=['GET'])
def get_recommend(user_id):
    global recommend_model, products_df, global_behavior_df
    
    # 每次请求都重新加载数据并训练，确保能感知到刚才的购买行为
    # (在大型生产环境中通常会用定时任务每小时训练一次)
    train_model()

    final_results = []
    
    # 记录该用户已经买过/看过的商品ID，避免重复推荐
    interacted_items = set()
    if global_behavior_df is not None and not global_behavior_df.empty:
        user_history = global_behavior_df[global_behavior_df["user_id"] == user_id]
        interacted_items = set(user_history["product_id"].tolist())

    # --- 阶段 1: 尝试协同过滤推荐 ---
    if recommend_model:
        try:
            # 找出所有没买过的商品作为候选
            all_pids = products_df["product_id"].tolist()
            candidates = [p for p in all_pids if p not in interacted_items]
            
            predictions = []
            for pid in candidates:
                # 预测评分: predict(uid, iid)
                # est: 预测出来的分数
                # details['was_impossible']: True 表示没找到邻居，用的是全局平均分
                pred = recommend_model.predict(user_id, pid)
               
                if pred.details['was_impossible']:
                    print(f"⚠️ 无法预测用户 {user_id} 对商品 {pid} 的评分: 数据太稀疏")
                else:
                    print(f"✅ 成功预测: 用户 {user_id} -> 商品 {pid} = {pred.est}")

                
                if not pred.details['was_impossible']:
                    predictions.append({"pid": pid, "score": pred.est})
            
            # 按预测分从高到低排序
            predictions.sort(key=lambda x: x["score"], reverse=True)
            
            # 取前 12 个
            top_preds = predictions[:12]
            
            for item in top_preds:
                # 从 products_df 里查详情
                row = products_df[products_df["product_id"] == item["pid"]].iloc[0]
                final_results.append({
                    "product_id": int(item["pid"]),
                    "name": row["name"],
                    "price": float(row["price"]),
                    "image_url": row["image_url"],
                    "reason": f"猜你喜欢 ", # (匹配度 {round(item['score'], 1)})可以给前端显示理由
                    "type": "cf" # 标记为协同过滤推荐
                })
        except Exception as e:
            print(f"协同过滤推荐出错: {e}")

    # --- 阶段 2: 保底机制 (冷启动/不足 9 个时启用) ---
    # 如果协同过滤没算出结果（比如新用户），或者结果太少，启用“热门 + 最新”混合推荐
    if len(final_results) < 9:
        need_count = 12 - len(final_results) # 努力补齐到 12 个
        print(f"ℹ️ 协同过滤结果不足，准备补充热门与最新商品共 {need_count} 个")
        
        # 排除掉 已经推荐的 和 已经买过的
        exclude_ids = list(interacted_items) + [x["product_id"] for x in final_results]
        
        # 1. 优先补充“全局热门商品” (占空缺名额的一半，比如缺12个则取6个)
        hot_count = need_count // 2 + need_count % 2
        added_hot = 0

        # 直接利用前面算好的 global_behavior_df，计算全站每个商品的总交互分 (总分越高的越热门)
        if global_behavior_df is not None and not global_behavior_df.empty:
            pop_series = global_behavior_df.groupby("product_id")["score"].sum().sort_values(ascending=False)
            hot_candidates = [pid for pid in pop_series.index if pid not in exclude_ids]
            
            for pid in hot_candidates[:hot_count]:
                product_rows = products_df[products_df["product_id"] == pid]
                if not product_rows.empty:
                    row = product_rows.iloc[0]
                    final_results.append({
                        "product_id": int(pid),
                        "name": row["name"],
                        "price": float(row["price"]),
                        "image_url": row["image_url"],
                        "reason": "全站热卖",
                        "type": "hot"
                    })
                    exclude_ids.append(pid)
                    added_hot += 1
        
        # 2. 剩余的名额用“最新商品”补齐
        remain_count = need_count - added_hot
        if remain_count > 0:
            latest_products = Product.query.filter(Product.id.notin_(exclude_ids))\
                .order_by(Product.id.desc())\
                .limit(remain_count).all()
                
            for p in latest_products:
                final_results.append({
                    "product_id": p.id,
                    "name": p.name,
                    "price": float(p.price),
                    "image_url": p.image_url,
                    "reason": "新品速递",
                    "type": "latest"
                })
            
    return jsonify({
        "code": 200,
        "msg": "success",
        "data": final_results
    })

