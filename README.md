# 电子商务网站

一个基于Flask的电子商务网站，支持商品管理、订单管理、用户管理等功能。
学号[202330453211]
姓名[郑烨]
班级[计科一班]

## 技术栈

- 后端框架: Flask
- 数据库: SQLAlchemy (支持SQLite/MySQL)
- ORM: Flask-SQLAlchemy
- 认证: Flask-Login
- 表单: Flask-WTF
- 迁移: Flask-Migrate
- 邮件: Flask-Mail
- 服务器: Gunicorn + Nginx

## 代码介绍

本项目采用模块化设计，使用Flask Blueprint将不同功能模块分离，便于维护和扩展。主要功能包括商品管理、订单管理、用户管理、购物车等核心电子商务功能。

## 项目结构


ecommerce_project/
├── app/
│   ├── admin/          # 管理员模块
│   ├── auth/           # 认证模块
│   ├── cart/           # 购物车模块
│   ├── main/           # 主模块
│   ├── models/         # 数据模型
│   ├── order/          # 订单模块
│   ├── shop/           # 商店模块
│   ├── static/         # 静态文件
│   ├── templates/      # 模板文件
│   ├── __init__.py     # 应用初始化
│   └── errors.py       # 错误处理
├── migrations/         # 数据库迁移
├── .env.example        # 环境变量示例
├── config.py           # 配置文件
├── requirements.txt    # 依赖列表
├── run.py              # 应用入口
└── README.md           # 项目说明


## 模块介绍

### 管理员模块 (admin)
负责网站后台管理功能，包括商品管理、订单管理、用户管理等。只有管理员用户可以访问此模块的功能。

### 认证模块 (auth)
处理用户注册、登录、密码重置等认证相关功能，基于Flask-Login实现用户会话管理。

### 购物车模块 (cart)
实现购物车功能，包括添加商品到购物车、修改购物车商品数量、删除购物车商品等。

### 主模块 (main)
包含网站的主要页面和通用功能，如首页、关于我们、联系我们等静态页面。

### 数据模型 (models)
定义项目的所有数据模型，包括用户、商品、订单、购物车等，使用SQLAlchemy ORM实现数据库操作。

### 订单模块 (order)
处理订单相关功能，包括创建订单、查看订单详情、取消订单等。

### 商店模块 (shop)
实现商品展示、搜索、分类浏览等前端商店功能，是用户主要交互的模块。

## Docker部署 (推荐)

### 1. 环境准备

确保服务器已安装Docker和Docker Compose：


# 更新系统
apt update && apt upgrade -y

# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 安装Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# 验证安装
docker --version
docker-compose --version


### 2. 部署步骤


# 克隆项目代码到服务器
cd /var/www
git clone <repository-url> ecommerce
cd ecommerce

# 启动容器服务
docker-compose up -d

# 查看服务状态
docker-compose ps


### 3. 环境配置

编辑docker-compose.yml文件中的环境变量（可选）：


nano docker-compose.yml


主要配置项：
- `SECRET_KEY`: 应用密钥，用于加密会话数据
- `MYSQL_ROOT_PASSWORD`: MySQL根密码
- `MYSQL_PASSWORD`: 应用数据库密码

### 4. 访问网站

部署完成后，可以通过以下方式访问网站：


# 通过公网IP访问
http://8.134.164.229



### 5. 常见操作

# 查看应用日志
docker-compose logs -f web

# 查看数据库日志
docker-compose logs -f db

# 查看Nginx日志
docker-compose logs -f nginx

# 重启所有服务
docker-compose restart

# 停止所有服务
docker-compose down

# 查看容器状态
docker-compose ps


## 常见问题解决

### 1. 数据库连接错误

- 检查docker-compose.yml中的数据库配置是否正确
- 确保数据库服务正在运行: `docker-compose logs -f db`

### 2. 404/400错误

- 检查路由配置是否正确
- 确保表单中包含CSRF令牌
- 检查URL路径是否与路由匹配

### 3. 库存恢复问题

取消订单后，商品库存会自动恢复，确保以下代码在路由中存在：

```python
# 取消订单时恢复库存
for item in order.items:
    product = Product.query.get(item.product_id)
    if product:
        product.stock += item.quantity
db.session.commit()
```

### 4. 生产环境调试

- 查看应用日志: `docker-compose logs -f web`
- 查看Nginx日志: `docker-compose logs -f nginx`
- 进入容器调试: `docker-compose exec web /bin/sh`

## 功能列表

### 1. 商品管理
- 添加、编辑、删除商品
- 商品分类管理
- 商品库存管理

### 2. 订单管理
- 查看订单列表
- 取消订单（恢复库存）
- 删除已取消订单
- 订单状态管理

### 3. 用户管理
- 用户列表查看
- 用户信息管理
- 管理员权限控制

### 4. 仪表盘
- 总订单数（仅统计pending状态）
- 总销售额（仅统计pending状态）
- 商品库存统计

### 5. 用户功能
- 用户注册/登录
- 购物车管理
- 订单管理
- 个人信息管理

