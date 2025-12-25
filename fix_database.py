import sqlite3
import os

# 数据库文件路径
db_path = 'ecommerce.db'
print(f"连接到数据库: {db_path}")

# 连接到SQLite数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
print("\n数据库连接成功")

try:
    # 1. 为orders表添加payment_method列
    print("\n1. 检查并添加orders表的payment_method列...")
    cursor.execute("PRAGMA table_info(orders)")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]
    
    if 'payment_method' not in column_names:
        cursor.execute("ALTER TABLE orders ADD COLUMN payment_method TEXT")
        print("   ✓ payment_method列已添加")
    else:
        print("   ✓ payment_method列已存在")
    
    # 2. 修复cart_items表的外键约束
    print("\n2. 检查并修复cart_items表的外键约束...")
    
    # 获取cart_items表的当前创建语句
    cursor.execute("SELECT sql FROM sqlite_master WHERE name='cart_items' AND type='table'")
    create_table_sql = cursor.fetchone()[0]
    print(f"   当前表结构: {create_table_sql}")
    
    # 检查外键是否指向carts表
    if 'REFERENCES carts' in create_table_sql:
        print("   发现外键指向carts表，需要修复...")
        
        # SQLite无法直接修改外键约束，所以需要重建表
        # 1. 创建临时表
        cursor.execute("""
            CREATE TABLE cart_items_new (
                id INTEGER PRIMARY KEY,
                cart_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER,
                added_at DATETIME,
                FOREIGN KEY (cart_id) REFERENCES cart (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        """)
        
        # 2. 复制数据
        cursor.execute("INSERT INTO cart_items_new SELECT * FROM cart_items")
        
        # 3. 删除旧表
        cursor.execute("DROP TABLE cart_items")
        
        # 4. 重命名新表
        cursor.execute("ALTER TABLE cart_items_new RENAME TO cart_items")
        
        print("   ✓ 外键约束已修复为指向cart表")
    else:
        print("   ✓ 外键约束已经正确")
    
    # 3. 检查最终的表结构
    print("\n3. 检查最终表结构:")
    
    # 检查orders表
    print("   orders表列:")
    cursor.execute("PRAGMA table_info(orders)")
    for col in cursor.fetchall():
        print(f"     - {col[1]}: {col[2]} (NULLABLE: {col[3]})")
    
    # 检查cart_items表
    print("   cart_items表列:")
    cursor.execute("PRAGMA table_info(cart_items)")
    for col in cursor.fetchall():
        print(f"     - {col[1]}: {col[2]} (NULLABLE: {col[3]})")
    
    print("\n4. 检查外键约束:")
    cursor.execute("PRAGMA foreign_key_list(cart_items)")
    fks = cursor.fetchall()
    for fk in fks:
        print(f"   - 列 {fk[3]} -> {fk[2]}.{fk[4]}")
    
    # 提交所有更改
    conn.commit()
    print("\n✅ 数据库修复完成!")
    
except Exception as e:
    print(f"\n❌ 修复过程中发生错误: {e}")
    conn.rollback()
    import traceback
    traceback.print_exc()
finally:
    # 关闭连接
    conn.close()
    print("\n数据库连接已关闭")