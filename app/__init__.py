from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail  # 添加邮件扩展
from flask_migrate import Migrate
from config import config

# 初始化扩展
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()  # 添加邮件对象
migrate = Migrate()

# 配置登录视图
login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录以访问此页面'
login_manager.login_message_category = 'info'
login_manager.session_protection = 'strong'

def create_app(config_name='default'):
    """应用工厂函数"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 初始化配置
    config[config_name].init_app(app)
    
    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)  # 初始化邮件
    migrate.init_app(app, db)
    
    # 注册蓝图
    from app.auth import auth as auth_blueprint
    from app.main import main as main_blueprint
    from app.shop import shop as shop_blueprint
    from app.admin import admin as admin_blueprint
    from app.cart import cart as cart_blueprint
    from app.order import order as order_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(main_blueprint)
    app.register_blueprint(shop_blueprint, url_prefix='/shop')
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(cart_blueprint, url_prefix='/cart')
    app.register_blueprint(order_blueprint, url_prefix='/order')
    
    # 注册错误处理器
    from app.errors import register_error_handlers
    register_error_handlers(app)
    
    # 注册上下文处理器
    from app.context_processors import inject_now, inject_categories, inject_cart_info
    app.context_processor(inject_now)
    app.context_processor(inject_categories)
    app.context_processor(inject_cart_info)
    
    # 创建数据库表（仅用于开发）
    if app.config.get('DEBUG'):
        with app.app_context():
            db.create_all()
            from app.models import User, Category, Product
            # 创建默认数据
            create_default_data()
    
    return app

def create_default_data():
    """创建默认数据"""
    from werkzeug.security import generate_password_hash
    from datetime import datetime
    
    from app.models import User, Category, Product
    
    # 创建默认管理员
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com',
            phone='13800138000',
            address='管理员地址',
            is_admin=True,
            is_active=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
    
    # 创建默认用户
    user = User.query.filter_by(username='testuser').first()
    if not user:
        user = User(
            username='testuser',
            email='test@example.com',
            phone='13900139000',
            address='测试用户地址',
            is_active=True
        )
        user.set_password('test123')
        db.session.add(user)
    
    # 创建默认分类
    if Category.query.count() == 0:
        categories = [
            Category(name='电子产品', description='手机、电脑、平板等'),
            Category(name='服装鞋帽', description='男女服装、鞋子等'),
            Category(name='图书音像', description='书籍、音乐、电影等'),
            Category(name='家居用品', description='家具、厨具、装饰品等'),
            Category(name='食品饮料', description='零食、饮料、生鲜等'),
            Category(name='美妆个护', description='化妆品、护肤品等'),
            Category(name='运动户外', description='运动器材、户外装备等'),
            Category(name='母婴玩具', description='母婴用品、儿童玩具等'),
        ]
        for category in categories:
            db.session.add(category)
    
    # 创建测试商品
    if Product.query.count() == 0:
        products = [
            Product(
                name='iPhone 15 Pro',
                description='最新款苹果手机，A17 Pro芯片，超视网膜XDR显示屏',
                price=7999.00,
                stock=50,
                category_id=1,
                image='iphone15.jpg'
            ),
            Product(
                name='华为Mate 60 Pro',
                description='华为旗舰手机，卫星通话功能，麒麟9000S芯片',
                price=6999.00,
                stock=30,
                category_id=1,
                image='mate60.jpg'
            ),
            Product(
                name='小米14 Ultra',
                description='小米最新影像旗舰，徕卡联合研发',
                price=5999.00,
                stock=100,
                category_id=1,
                image='xiaomi14.jpg'
            ),
            Product(
                name='联想拯救者Y9000P',
                description='高性能游戏本，i9处理器，RTX 4060显卡',
                price=10999.00,
                stock=20,
                category_id=1,
                image='lenovo.jpg'
            ),
            Product(
                name='耐克Air Max 270',
                description='新款跑步鞋，超大Air气垫，透气舒适',
                price=899.00,
                stock=200,
                category_id=2,
                image='nike.jpg'
            ),
            Product(
                name='编程珠玑（第2版）',
                description='程序员必读经典，算法与程序设计',
                price=89.90,
                stock=500,
                category_id=3,
                image='book1.jpg'
            ),
            Product(
                name='Python编程：从入门到实践（第2版）',
                description='Python入门最佳书籍，包含实际项目',
                price=99.00,
                stock=300,
                category_id=3,
                image='book2.jpg'
            ),
            Product(
                name='戴森V12吸尘器',
                description='无线吸尘器，激光探测灰尘',
                price=4490.00,
                stock=25,
                category_id=4,
                image='dyson.jpg'
            ),
            Product(
                name='星巴克咖啡豆',
                description='中度烘焙，阿拉比卡咖啡豆',
                price=129.00,
                stock=150,
                category_id=5,
                image='coffee.jpg'
            ),
            Product(
                name='乐高经典创意系列',
                description='1500颗粒，激发创造力',
                price=399.00,
                stock=80,
                category_id=8,
                image='lego.jpg'
            ),
        ]
        for product in products:
            db.session.add(product)
    
    db.session.commit()
    print("默认数据创建完成！")
