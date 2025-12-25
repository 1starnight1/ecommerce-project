from app import create_app, db
import os

# 创建应用实例
app = create_app()

# 在应用上下文中工作
with app.app_context():
    print("Flask应用配置信息:")
    print(f"  DEBUG: {app.config.get('DEBUG')}")
    print(f"  SQLALCHEMY_DATABASE_URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    
    # 检查数据库文件的绝对路径
    if app.config.get('SQLALCHEMY_DATABASE_URI').startswith('sqlite:///'):
        db_file = app.config.get('SQLALCHEMY_DATABASE_URI')[10:]
        if db_file.startswith('/'):
            absolute_path = db_file
        else:
            absolute_path = os.path.join(app.root_path, db_file)
        print(f"  数据库文件绝对路径: {absolute_path}")
        print(f"  文件是否存在: {os.path.exists(absolute_path)}")
    
    # 重新创建所有表
    print("\n重新创建所有数据库表...")
    db.drop_all()  # 删除所有现有表
    db.create_all()  # 创建所有新表
    print("  ✓ 表创建完成")
    
    # 检查orders表结构
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    if inspector.has_table('orders'):
        print("\norders表结构:")
        columns = inspector.get_columns('orders')
        for col in columns:
            print(f"  - {col['name']}: {col['type']} (NULLABLE: {col['nullable']})")
    
    # 检查cart_items表的外键
    if inspector.has_table('cart_items'):
        print("\ncart_items表外键:")
        fks = inspector.get_foreign_keys('cart_items')
        for fk in fks:
            print(f"  - {fk['constrained_columns'][0]} -> {fk['referred_table']}.{fk['referred_columns'][0]}")

print("\n数据库初始化完成！")