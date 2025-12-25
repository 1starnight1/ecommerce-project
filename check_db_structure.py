from app import create_app, db
from app.models import User, Product, Category, Order, Cart, CartItem, OrderItem, Review, UserLog

# 创建应用实例
app = create_app()

# 在应用上下文中工作
with app.app_context():
    print("检查数据库结构...")
    
    # 检查并创建所有表
    print("创建/更新所有表...")
    db.create_all()
    
    # 检查orders表是否有payment_method和notes列
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    
    if inspector.has_table('orders'):
        print("\n检查orders表结构:")
        columns = inspector.get_columns('orders')
        column_names = [col['name'] for col in columns]
        
        for col in columns:
            print(f"  - {col['name']}: {col['type']} (NULLABLE: {col['nullable']})")
        
        if 'payment_method' not in column_names:
            print("  ⚠️  缺少payment_method列")
        if 'notes' not in column_names:
            print("  ⚠️  缺少notes列")
        else:
            print("  ✓ orders表结构完整")
    else:
        print("  ⚠️  orders表不存在")
    
    # 检查cart表和cart_items表的关系
    print("\n检查购物车相关表:")
    if inspector.has_table('cart'):
        print("  ✓ cart表存在")
        columns = inspector.get_columns('cart')
        for col in columns:
            print(f"    - {col['name']}: {col['type']}")
    else:
        print("  ⚠️  cart表不存在")
    
    if inspector.has_table('cart_items'):
        print("  ✓ cart_items表存在")
        columns = inspector.get_columns('cart_items')
        for col in columns:
            print(f"    - {col['name']}: {col['type']}")
        
        # 检查外键
        fks = inspector.get_foreign_keys('cart_items')
        if fks:
            print("  外键约束:")
            for fk in fks:
                print(f"    - {fk['constrained_columns'][0]} -> {fk['referred_table']}.{fk['referred_columns'][0]}")
    else:
        print("  ⚠️  cart_items表不存在")
    
    print("\n数据库检查完成!")