#!/usr/bin/env python3
"""
创建一个测试订单，用于测试用户端取消订单功能
"""

from app import create_app, db
from app.models import User, Product, Order, OrderItem
from datetime import datetime
import random

def create_test_order():
    """创建一个测试订单"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("创建测试订单")
        print("=" * 60)
        
        # 获取测试用户
        user = User.query.filter_by(username='testuser').first()
        if not user:
            print("✗ 未找到测试用户 testuser")
            return False
        print(f"✓ 找到测试用户: {user.username}")
        
        # 获取可用商品
        products = Product.query.filter(Product.stock > 0).all()
        if not products:
            print("✗ 没有可用商品")
            return False
        print(f"✓ 找到 {len(products)} 个可用商品")
        
        # 随机选择一个商品
        selected_product = random.choice(products)
        quantity = 1
        
        if selected_product.stock < quantity:
            print(f"✗ 商品 {selected_product.name} 库存不足")
            return False
        
        # 创建订单
        order = Order(
            order_number=Order.generate_order_number(),
            user_id=user.id,
            total_amount=selected_product.price * quantity,
            status='pending',
            shipping_address=user.address or '测试用户地址',
            payment_method='credit_card',
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.session.add(order)
        db.session.flush()  # 获取订单ID
        
        # 创建订单项
        order_item = OrderItem(
            order_id=order.id,
            product_id=selected_product.id,
            quantity=quantity,
            price=selected_product.price,
            subtotal=selected_product.price * quantity
        )
        
        db.session.add(order_item)
        
        # 减少商品库存
        selected_product.stock -= quantity
        
        # 提交更改
        db.session.commit()
        
        print(f"✓ 创建订单成功！")
        print(f"  订单ID: {order.id}")
        print(f"  商品: {selected_product.name} (ID: {selected_product.id})")
        print(f"  数量: {quantity}")
        print(f"  总价: ¥{order.total_amount}")
        print(f"  状态: {order.status}")
        
        return True

if __name__ == '__main__':
    create_test_order()