"""
应用启动文件
"""
import os
from app import create_app, db
from app.models import User, Product, Order, OrderItem, CartItem, UserLog
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    """为Flask shell添加上下文"""
    return {
        'db': db,
        'User': User,
        'Product': Product,
        'Order': Order,
        'OrderItem': OrderItem,
        'CartItem': CartItem,
        'UserLog': UserLog
    }


@app.cli.command()
def init_db():
    """初始化数据库"""
    from datetime import datetime, timedelta
    import random

    db.create_all()

    # 创建管理员账户
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@example.com',
            phone='13800138000',
            address='北京市海淀区',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)

        # 创建测试用户
        test_user = User(
            username='testuser',
            email='test@example.com',
            phone='13800138001',
            address='上海市徐汇区'
        )
        test_user.set_password('test123')
        db.session.add(test_user)

        # 添加示例商品
        sample_products = [
            Product(
                name='笔记本电脑',
                description='高性能游戏本，配备最新处理器和显卡',
                price=6999.00,
                stock=10,
                category='电子产品',
                sku='PROD001',
                image='laptop.jpg'
            ),
            Product(
                name='智能手机',
                description='最新款智能手机，超长续航',
                price=3999.00,
                stock=20,
                category='电子产品',
                sku='PROD002',
                image='phone.jpg'
            ),
            Product(
                name='无线耳机',
                description='降噪蓝牙耳机',
                price=599.00,
                stock=30,
                category='电子产品',
                sku='PROD003'
            ),
            Product(
                name='T恤衫',
                description='纯棉舒适T恤，多色可选',
                price=99.00,
                stock=50,
                category='服装',
                sku='PROD004'
            ),
            Product(
                name='运动鞋',
                description='专业运动跑鞋',
                price=299.00,
                stock=30,
                category='服装',
                sku='PROD005'
            ),
        ]

        for product in sample_products:
            db.session.add(product)

        db.session.commit()
        print('数据库初始化完成！')
        print('管理员账号：admin / admin123')
        print('测试用户账号：testuser / test123')
        print(f'已创建 {len(sample_products)} 个商品')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)