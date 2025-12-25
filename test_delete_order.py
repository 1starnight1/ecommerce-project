from flask import Flask
from app import create_app, db
from app.models import User, Order
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = create_app()

with app.app_context():
    # 创建一个已取消的测试订单
    admin = User.query.filter_by(username='admin').first()
    if admin:
        # 检查是否已存在cancelled状态的订单
        cancelled_order = Order.query.filter_by(status='cancelled').first()
        if not cancelled_order:
            # 创建一个cancelled状态的测试订单
            test_order = Order(
                user_id=admin.id,
                order_number='TEST_DELETE_001',
                total_amount=100.00,
                payment_method='alipay',
                status='cancelled',
                shipping_address='测试删除地址'
            )
            db.session.add(test_order)
            db.session.commit()
            logger.info(f"创建测试删除订单: {test_order.id}")
            order_id = test_order.id
        else:
            order_id = cancelled_order.id
            logger.info(f"使用现有取消订单: {order_id}")
        
        # 启动测试客户端
        client = app.test_client()
        
        # 获取登录页面并提取CSRF令牌
        login_page_response = client.get('/auth/login')
        logger.info(f"获取登录页面状态码: {login_page_response.status_code}")
        
        import re
        csrf_login_match = re.search(r'<input type="hidden" name="csrf_token" value="([^"\']+)"', login_page_response.data.decode('utf-8'))
        if csrf_login_match:
            login_csrf_token = csrf_login_match.group(1)
            logger.info(f"登录页面CSRF令牌: {login_csrf_token}")
            
            # 登录管理员
            login_response = client.post('/auth/login', data={
                'username': 'admin',
                'password': 'admin123',
                'csrf_token': login_csrf_token
            })
            logger.info(f"登录状态码: {login_response.status_code}")
            
            # 获取订单管理页面并提取CSRF令牌
            order_manage_response = client.get('/admin/orders')
            logger.info(f"获取订单管理页面状态码: {order_manage_response.status_code}")
            
            csrf_match = re.search(r'<input type="hidden" name="csrf_token" value="([^"\']+)"', order_manage_response.data.decode('utf-8'))
            if csrf_match:
                csrf_token = csrf_match.group(1)
                logger.info(f"从页面提取的CSRF令牌: {csrf_token}")
                
                # 尝试删除订单
                delete_response = client.post(f'/admin/orders/{order_id}/delete', data={
                    'csrf_token': csrf_token
                })
                logger.info(f"删除订单状态码: {delete_response.status_code}")
                logger.info(f"响应头: {dict(delete_response.headers)}")
                
                # 检查订单是否已被删除
                deleted_order = Order.query.get(order_id)
                if deleted_order:
                    logger.error(f"订单删除失败，订单仍然存在: {deleted_order.id}, 状态: {deleted_order.status}")
                else:
                    logger.info(f"订单删除成功，订单ID: {order_id}")
            else:
                logger.error("无法从页面提取CSRF令牌")
        else:
            logger.error("无法从登录页面提取CSRF令牌")