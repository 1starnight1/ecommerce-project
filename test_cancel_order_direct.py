from app import create_app, db
from app.models import User, Order
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = create_app()

with app.app_context():
    # 获取管理员用户
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        logger.error("管理员用户不存在")
        exit(1)
    
    # 获取或创建测试订单
    order = Order.query.filter_by(status='pending').first()
    if not order:
        # 创建测试订单
        from datetime import datetime
        order = Order(
            user_id=admin.id,
            order_number='TEST-2025-001',
            total_amount=299.99,
            payment_method='alipay',
            status='pending',
            shipping_address='测试地址',
            shipping_name='测试用户',
            shipping_phone='13800138000',
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.session.add(order)
        db.session.commit()
        logger.info(f"创建测试订单: {order.id}")
    else:
        logger.info(f"使用现有测试订单: {order.id}, 状态: {order.status}")
    
    # 直接调用取消订单函数进行测试
    from app.admin.routes import cancel_order
    from flask import request, session
    from flask_login import login_user
    
    # 创建模拟请求上下文
    with app.test_request_context(f'/admin/orders/{order.id}/cancel', method='POST'):
        # 登录用户
        login_user(admin)
        
        # 手动设置session
        session['_user_id'] = str(admin.id)
        session['_fresh'] = True
        
        # 尝试调用取消订单函数
        try:
            response = cancel_order(order.id)
            logger.info(f"取消订单成功，重定向到: {response.location}")
            
            # 检查订单状态
            updated_order = db.session.query(Order).get(order.id)
            logger.info(f"更新后订单状态: {updated_order.status}")
            
            if updated_order.status == 'cancelled':
                logger.info("✅ 取消订单功能测试成功！")
            else:
                logger.error("❌ 订单状态未更新为取消")
                
        except Exception as e:
            logger.error(f"❌ 取消订单失败: {str(e)}")
            import traceback
            traceback.print_exc()