# E-Commerce 商城前端项目 (frontend2)

本项目是基于 **Vue 3** 构建的电子商务平台前端系统，采用了前后端分离架构（后端为 Flask API）。

## 💻 核心技术栈

- **前端框架**: Vue.js `v3.2.13` (Vue 3)
- **UI 组件库**: Element Plus `v2.10.3` (包含图标库 `@element-plus/icons-vue`)
- **路由管理**: Vue Router `v4.0.3`
- **状态管理**: Vuex `v4.0.0`
- **网络请求**: Axios `v1.10.0` / 原生 Fetch
- **日期处理**: Dayjs `v1.11.13`
- **构建工具**: Vue CLI `v5.0.0` (基于 Webpack)

## 📦 主要功能特性

- **买家版**: 
  - 用户注册/登录、基本资料维护与头像上传。
  - 商品浏览、商品推荐、分类展示。
  - 购物车管理、收货地址管理。
  - 订单创建、在线充值、售后/退款状态流转。
  - 我的收藏、商品评价与点赞等互动。
- **商家版**: 
  - 商家仪表盘（数据统计分析）。
  - 商品多维度管理（上架、下架、编辑）。
  - 订单发货与退款审批管理。

## 🚀 部署与运行说明

本项目为前后端分离架构，需要分别启动**后端服务(Flask)**和**前端开发服务器(Vue)**。

### 🔧 1. 后端部署与启动 (Flask Backend)
后端环境依赖 Python 3.8+，所需依赖已在 `backend/requirements.txt` 中配置好。

**步骤 1：进入后端目录**
```bash
cd backend
```

**步骤 2：创建虚拟环境并激活（推荐）**
```bash
python -m venv venv
# Windows 激活方式:
venv\Scripts\activate
# Mac/Linux 激活方式:
source venv/bin/activate
```

**步骤 3：安装依赖**
```bash
pip install -r requirements.txt
# 或者如果你使用的是由于网络/环境配置指定的另一个版本依赖文件：
# pip install -r py39_requirements_pip.txt
```

**步骤 4：初始化数据库与测试数据**
根据项目中的初始化脚本运行：
```bash
python chushihua.py 
# 或 python init_data.py
```

**步骤 5：启动后端接口服务**
```bash
python app.py
```
> **提示**: 后端服务默认会运行在 `http://127.0.0.1:5000/`，并已配置了跨域(CORS)和 `static/uploads` 静态资源反向代理。


### 🎨 2. 前端部署与启动 (Vue Frontend)
确保你已经安装了 [Node.js](https://nodejs.org/) (建议版本 v16+)。

**步骤 1：进入前端包目录**
```bash
cd frontend2
```

**步骤 2：安装项目依赖 (一键安装)**
```bash
npm install
```

**步骤 3：启动开发服务器 (支持热更新)**
```bash
npm run serve
```
> **提示**: 启动成功后，浏览器中访问 `http://localhost:8080/` 即可看到商城前端页面。前端发送的所有接口请求会自动向后端的 `:5000` 端口发起。

### 🚢 3. 生产环境部署 (Production Deployment)

如果你需要将项目正式部署到公网服务器，流程如下：

#### 前端静态化打包
在 `frontend2` 目录下运行：
```bash
npm run build
```
打包完成后会在该目录下生成一个 `dist/` 文件夹。将该文件夹下的所有静态文件复制到你的 Web 服务器（如 Nginx、Apache）的对应目录。

#### Nginx 配置参考示例
```nginx
server {
    listen 80;
    server_name your_domain.com;

    # 前端静态文件路由
    location / {
        root /path/to/your/frontend2/dist;  # 替换成实际打包后的 dist 目录路径
        index index.html;
        try_files $uri $uri/ /index.html;   # 解决 Vue 路由前端History模式下 404 的问题
    }

    # 后端接口反向代理
    location /api/ {
        proxy_pass http://127.0.0.1:5000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # 后端静态资源（例如用户头像、商品图在后端的 static 下）
    location /static/ {
        proxy_pass http://127.0.0.1:5000/static/;
    }
}
```
