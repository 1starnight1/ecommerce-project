import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

from app import create_app, db

# 创建应用实例
app = create_app()


@app.shell_context_processor
def make_shell_context():
    """为Flask shell添加上下文"""
    from app import db
    from app.models import User, Product, Category, Order, Cart, CartItem, OrderItem, Review, UserLog
    return {
        'db': db,
        'User': User,
        'Product': Product,
        'Category': Category,
        'Order': Order,
        'Cart': Cart,
        'CartItem': CartItem,
        'OrderItem': OrderItem,
        'Review': Review,
        'UserLog': UserLog
    }


# 数据库初始化函数
def init_database():
    """初始化数据库和默认数据"""
    print("=" * 60)
    print("正在初始化数据库...")
    print("=" * 60)

    try:
        # 创建所有表
        db.create_all()
        print("✓ 数据库表已检查/创建")

        # 创建默认管理员
        from app.models import User
        from werkzeug.security import generate_password_hash
        from datetime import datetime

        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@example.com',
                phone='13800138000',
                address='广东省广州市天河区',
                is_admin=True,
                is_active=True,
                created_at=datetime.utcnow()
            )
            admin.set_password('admin123')
            db.session.add(admin)
            print("✓ 创建管理员: admin / admin123")
        else:
            print(f"✓ 管理员账户已存在: {admin.username}")

        # 创建测试用户
        test_user = User.query.filter_by(username='testuser').first()
        if not test_user:
            test_user = User(
                username='testuser',
                email='test@example.com',
                phone='13900139000',
                address='广东省深圳市南山区',
                is_active=True,
                created_at=datetime.utcnow()
            )
            test_user.set_password('test123')
            db.session.add(test_user)
            print("✓ 创建测试用户: testuser / test123")
        else:
            print(f"✓ 测试用户已存在: {test_user.username}")

        # 创建默认分类
        from app.models import Category
        if Category.query.count() == 0:
            categories = [
                Category(name='电子产品', description='手机、电脑、平板等数码产品'),
                Category(name='服装鞋帽', description='男女服装、鞋子、配饰等'),
                Category(name='图书音像', description='书籍、音乐、电影等'),
                Category(name='家居用品', description='家具、厨具、装饰品等'),
                Category(name='食品饮料', description='零食、饮料、生鲜等'),
                Category(name='美妆个护', description='化妆品、护肤品、个人护理等'),
                Category(name='运动户外', description='运动器材、户外装备等'),
                Category(name='母婴玩具', description='母婴用品、儿童玩具等'),
            ]
            for category in categories:
                db.session.add(category)
            print(f"✓ 创建了 {len(categories)} 个默认分类")
        else:
            print(f"✓ 已有 {Category.query.count()} 个分类")

        # 创建测试商品
        from app.models import Product
        if Product.query.count() == 0:
            from random import uniform, randint

            products = [
                Product(
                    name='iPhone 15 Pro',
                    description='最新款苹果手机，A17 Pro芯片，超视网膜XDR显示屏',
                    price=7999.00,
                    stock=50,
                    category_id=1,
                    image='default_product.png'
                ),
                Product(
                    name='华为Mate 60 Pro',
                    description='华为旗舰手机，卫星通话功能，麒麟9000S芯片',
                    price=6999.00,
                    stock=30,
                    category_id=1,
                    image='default_product.png'
                ),
                Product(
                    name='小米14 Ultra',
                    description='小米最新影像旗舰，徕卡联合研发，骁龙8 Gen3',
                    price=5999.00,
                    stock=100,
                    category_id=1,
                    image='default_product.png'
                ),
                Product(
                    name='联想拯救者Y9000P',
                    description='高性能游戏本，i9-14900HX处理器，RTX 4060显卡',
                    price=10999.00,
                    stock=20,
                    category_id=1,
                    image='default_product.png'
                ),
                Product(
                    name='耐克Air Max 270',
                    description='新款跑步鞋，超大Air气垫，透气舒适',
                    price=899.00,
                    stock=200,
                    category_id=2,
                    image='default_product.png'
                ),
                Product(
                    name='编程珠玑（第2版）',
                    description='程序员必读经典，算法与程序设计',
                    price=89.90,
                    stock=500,
                    category_id=3,
                    image='default_product.png'
                ),
                Product(
                    name='Python编程：从入门到实践（第2版）',
                    description='Python入门最佳书籍，包含实际项目',
                    price=99.00,
                    stock=300,
                    category_id=3,
                    image='default_product.png'
                ),
                Product(
                    name='戴森V12吸尘器',
                    description='无线吸尘器，激光探测灰尘，轻便强力',
                    price=4490.00,
                    stock=25,
                    category_id=4,
                    image='default_product.png'
                ),
                Product(
                    name='星巴克咖啡豆',
                    description='中度烘焙，阿拉比卡咖啡豆，250g',
                    price=129.00,
                    stock=150,
                    category_id=5,
                    image='default_product.png'
                ),
                Product(
                    name='乐高经典创意系列',
                    description='1500颗粒，激发创造力',
                    price=399.00,
                    stock=80,
                    category_id=8,
                    image='default_product.png'
                ),
            ]
            for product in products:
                db.session.add(product)
            print(f"✓ 创建了 {len(products)} 个测试商品")
        else:
            print(f"✓ 已有 {Product.query.count()} 个商品")

        # 提交所有更改
        db.session.commit()
        print("✓ 数据库初始化完成")

    except Exception as e:
        db.session.rollback()
        print(f"✗ 数据库初始化失败: {e}")
        import traceback
        traceback.print_exc()

    print("=" * 60)
    return True


# 只在开发环境或显式请求时初始化数据库
if app.config.get('DEBUG') or os.environ.get('INIT_DATABASE') == 'True':
    with app.app_context():
        init_database()

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("电子商务网站启动成功！")
    print("=" * 60)
    print("\n访问信息:")
    print("  主页: http://127.0.0.1:5000")
    print("  管理员登录: http://127.0.0.1:5000/auth/login")
    print("  管理员账号: admin / admin123")
    print("  测试用户: testuser / test123")
    print("\n按 Ctrl+C 停止服务器")
    print("=" * 60 + "\n")

    app.run(
        debug=True,
        host=os.environ.get('FLASK_HOST', '0.0.0.0'),
        port=int(os.environ.get('FLASK_PORT', 5000))
    )