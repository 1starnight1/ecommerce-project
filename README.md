# 电子商务网站

一个基于Flask的电子商务网站，支持商品管理、订单管理、用户管理等功能。

## 技术栈

- **后端框架**: Flask
- **数据库**: SQLAlchemy (支持SQLite/MySQL)
- **ORM**: Flask-SQLAlchemy
- **认证**: Flask-Login
- **表单**: Flask-WTF
- **迁移**: Flask-Migrate
- **邮件**: Flask-Mail
- **服务器**: Gunicorn + Nginx
- **部署**: Supervisor

## 开发环境配置

### 1. 克隆项目

```bash
git clone <repository-url>
cd ecommerce_project
```

### 2. 创建虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

**注意**：如果您使用MySQL数据库，确保requirements.txt中包含以下依赖：
- `pymysql`：MySQL数据库驱动
- `cryptography`：支持MySQL的sha256_password认证方法
- `python-dotenv`：加载环境变量

### 4. 配置环境变量

复制 `.env.example` 文件并重命名为 `.env`，根据需要修改配置：

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

### 5. 启动开发服务器

```bash
python run.py
```

访问 http://127.0.0.1:5000 查看网站

## 生产环境部署 (阿里云ECS)

### 1. 环境准备

- 选择Ubuntu镜像 (推荐22.04 LTS)
- 实例规格: ecs.e-c1m1.large (或根据需求选择)
- 安全组配置: 开放80、443、22端口

### 2. 系统初始化

```bash
# 连接服务器
ssh root@your-server-ip

# 更新系统
apt update && apt upgrade -y

# 安装必要软件
apt install -y git python3-pip python3-venv nginx supervisor mysql-server
```

### 3. 配置MySQL

```bash
# 安全配置
mysql_secure_installation

# 创建数据库和用户
mysql -u root -p

CREATE DATABASE ecommerce CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'ecommerce_user'@'localhost' IDENTIFIED BY 'your-strong-password';
GRANT ALL PRIVILEGES ON ecommerce.* TO 'ecommerce_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 4. 克隆项目

```bash
cd /var/www
git clone <repository-url> ecommerce
cd ecommerce
```

### 5. 安装项目依赖

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install --upgrade pip
pip install -r requirements.txt
```

### 6. 配置环境变量

```bash
# 创建.env文件
nano .env

# 输入配置内容
FLASK_ENV=production
SECRET_KEY=your-secure-secret-key
DATABASE_URL=mysql+pymysql://ecommerce_user:your-strong-password@localhost/ecommerce
DEBUG=False
INIT_DATABASE=False

# 保存并退出
Ctrl+O, Enter, Ctrl+X
```

### 7. 执行数据库迁移

```bash
# 激活虚拟环境
source venv/bin/activate

# 初始化迁移（如果没有migrations目录）
flask db init

# 创建迁移脚本
flask db migrate -m "Initial migration"

# 执行迁移
flask db upgrade
```

### 8. 配置Gunicorn

```bash
# 创建启动脚本
nano gunicorn_start.sh

# 输入以下内容
#!/bin/bash

source /var/www/ecommerce/venv/bin/activate
export FLASK_ENV=production
export SECRET_KEY=your-secure-secret-key
export DATABASE_URL=mysql+pymysql://ecommerce_user:your-strong-password@localhost/ecommerce
export DEBUG=False
export INIT_DATABASE=False

gunicorn -w 4 -b 0.0.0.0:5000 run:app

# 保存并退出
Ctrl+O, Enter, Ctrl+X

# 添加执行权限
chmod +x gunicorn_start.sh
```

### 9. 配置Nginx

```bash
# 创建Nginx配置文件
nano /etc/nginx/sites-available/ecommerce

# 输入以下内容
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/ecommerce/app/static;
    }

    location /uploads {
        alias /var/www/ecommerce/app/static/uploads;
    }
}

# 保存并退出
Ctrl+O, Enter, Ctrl+X

# 创建软链接
ln -s /etc/nginx/sites-available/ecommerce /etc/nginx/sites-enabled/

# 测试配置
nginx -t

# 重启Nginx
systemctl restart nginx
```

### 10. 配置Supervisor

```bash
# 创建Supervisor配置文件
nano /etc/supervisor/conf.d/ecommerce.conf

# 输入以下内容
[program:ecommerce]
command=/var/www/ecommerce/gunicorn_start.sh
directory=/var/www/ecommerce
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/www/ecommerce/logs/gunicorn.log
stderr_logfile=/var/www/ecommerce/logs/error.log

# 保存并退出
Ctrl+O, Enter, Ctrl+X

# 创建日志目录
mkdir -p /var/www/ecommerce/logs

# 启动Supervisor
systemctl start supervisor

# 重新加载配置
supervisorctl reread
supervisorctl update
supervisorctl start ecommerce
```

### 11. 配置防火墙

```bash
ufw allow 80
iptables -I INPUT -p tcp --dport 80 -j ACCEPT
```

## 一站式部署 (推荐)

### 1. 环境准备

确保服务器已安装Docker和Docker Compose：

```bash
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
```

### 2. 部署步骤

```bash
# 克隆项目代码到服务器
cd /var/www
git clone <repository-url> ecommerce
cd ecommerce

# 启动容器服务
docker-compose up -d

# 查看服务状态
docker-compose ps
```

### 3. 环境配置

编辑docker-compose.yml文件中的环境变量（可选）：

```bash
nano docker-compose.yml
```

主要配置项：
- `SECRET_KEY`: 应用密钥，用于加密会话数据
- `MYSQL_ROOT_PASSWORD`: MySQL根密码
- `MYSQL_PASSWORD`: 应用数据库密码

### 4. 访问网站

部署完成后，可以通过以下方式访问网站：

```bash
# 通过公网IP访问
http://your-server-ip

# 如果配置了域名
http://your-domain.com
```

### 5. 常见操作

```bash
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
```

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

## 开发命令

### 运行开发服务器
```bash
python run.py
```

### 执行数据库迁移
```bash
flask db migrate -m "Migration message"
flask db upgrade
```

### 初始化数据库
```bash
# 开发环境下自动初始化
# 生产环境下手动执行
INIT_DATABASE=True python run.py
```

### 测试代码
```bash
python -m pytest
```

## 项目结构

```
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
```

## 许可证

MIT License