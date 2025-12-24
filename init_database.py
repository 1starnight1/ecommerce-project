# init_database.py
import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Product, Order, OrderItem, CartItem, UserLog
from datetime import datetime, timedelta
import random

app = create_app()

with app.app_context():
    print("开始创建数据库表...")

    # 删除所有表（如果存在）
    db.drop_all()

    # 创建所有表
    db.create_all()
    print("✅ 数据库表创建完成")

    # 创建管理员账户
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@example.com',
            phone='13800138000',
            address='北京市海淀区',
            is_admin=True,
            is_active=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        print("✅ 创建管理员账户: admin / admin123")

    # 创建测试用户
    if not User.query.filter_by(username='testuser').first():
        test_user = User(
            username='testuser',
            email='test@example.com',
            phone='13800138001',
            address='上海市徐汇区',
            is_active=True
        )
        test_user.set_password('test123')
        db.session.add(test_user)
        print("✅ 创建测试用户: testuser / test123")

    # 添加示例商品
    sample_products = [
        Product(
            name='笔记本电脑',
            description='高性能游戏本，配备最新处理器和显卡',
            price=6999.00,
            stock=10,
            category='电子产品',
            sku='PROD001',
            image='laptop.jpg',
            is_active=True
        ),
        Product(
            name='智能手机',
            description='最新款智能手机，超长续航',
            price=3999.00,
            stock=20,
            category='电子产品',
            sku='PROD002',
            image='phone.jpg',
            is_active=True
        ),
        Product(
            name='无线耳机',
            description='降噪蓝牙耳机',
            price=599.00,
            stock=30,
            category='电子产品',
            sku='PROD003',
            is_active=True
        ),
        Product(
            name='T恤衫',
            description='纯棉舒适T恤，多色可选',
            price=99.00,
            stock=50,
            category='服装',
            sku='PROD004',
            is_active=True
        ),
        Product(
            name='运动鞋',
            description='专业运动跑鞋',
            price=299.00,
            stock=30,
            category='服装',
            sku='PROD005',
            is_active=True
        ),
    ]

    for product in sample_products:
        if not Product.query.filter_by(sku=product.sku).first():
            db.session.add(product)

    print(f"✅ 创建 {len(sample_products)} 个商品")

    # 提交所有更改
    db.session.commit()
    print("✅ 数据提交完成")

    print("\n" + "=" * 50)
    print("🎉 数据库初始化完成！")
    print("=" * 50)
    print("\n现在可以:")
    print("1. 使用 admin / admin123 登录")
    print("2. 使用 testuser / test123 登录")
    print("3. 访问管理后台: http://127.0.0.1:5000/admin")