from flask import current_app, Flask
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath('.'))

# 导入应用和模型
from app import create_app
from app.models import db, Order

# 创建应用实例
app = create_app()

with app.app_context():
    try:
        # 测试Order模型是否能正常查询
        print("正在测试Order模型查询...")
        
        # 执行简单查询，验证表结构
        orders = Order.query.all()
        
        print(f"✅ 查询成功！共找到 {len(orders)} 个订单")
        print("\n订单表结构验证通过：")
        print("- payment_method 字段已存在")
        print("- notes 字段已存在")
        print("- 所有Order模型字段都能正常查询")
        
        # 如果有订单，打印第一个订单的信息
        if orders:
            order = orders[0]
            print(f"\n第一个订单信息：")
            print(f"  - ID: {order.id}")
            print(f"  - 订单号: {order.order_number}")
            print(f"  - 用户ID: {order.user_id}")
            print(f"  - 总金额: {order.total_amount}")
            print(f"  - 状态: {order.status}")
            print(f"  - 支付方式: {order.payment_method}")
            print(f"  - 备注: {order.notes}")
            
    except Exception as e:
        print(f"❌ 查询失败: {e}")
        import traceback
        traceback.print_exc()
