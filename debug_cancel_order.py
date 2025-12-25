from flask import Flask
from app import create_app, db
from app.models import User, Order
from werkzeug.security import check_password_hash
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = create_app()

with app.app_context():
    # 创建测试订单（确保有一个可取消的订单）
    if Order.query.count() == 0:
        # 获取管理员用户
        admin = User.query.filter_by(username='admin').first()
        if admin:
            # 创建测试订单
            test_order = Order(
                user_id=admin.id,
                order_number='TEST123456',
                total_amount=100.00,
                payment_method='alipay',
                status='pending',
                shipping_address='测试地址'
            )
            db.session.add(test_order)
            db.session.commit()
            logger.info(f"创建测试订单: {test_order.id}")
    else:
        # 确保有一个订单处于可取消状态
        order = Order.query.filter_by(status='pending').first()
        if not order:
            # 创建一个新的pending状态订单
            admin = User.query.filter_by(username='admin').first()
            if admin:
                test_order = Order(
                    user_id=admin.id,
                    order_number='TEST789012',
                    total_amount=200.00,
                    payment_method='wechat',
                    status='pending',
                    shipping_address='测试地址2'
                )
                db.session.add(test_order)
                db.session.commit()
                logger.info(f"创建新的pending状态测试订单: {test_order.id}")

    # 启动测试客户端
    client = app.test_client()
    
    # 获取登录页面以获取CSRF令牌
    login_page_response = client.get('/auth/login')
    logger.info(f"获取登录页面状态码: {login_page_response.status_code}")
    
    # 从登录页面提取CSRF令牌
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
    else:
        logger.error("无法从登录页面提取CSRF令牌")
        login_response = client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
    logger.info(f"登录状态码: {login_response.status_code}")
    
    # 获取订单ID - 确保是可取消状态的订单
    order = Order.query.filter(Order.status.in_(['pending', 'paid'])).first()
    if order:
        order_id = order.id
        logger.info(f"测试订单ID: {order_id}, 状态: {order.status}")
        
        # 获取订单管理页面以获取CSRF令牌
        order_manage_response = client.get('/admin/orders')
        logger.info(f"获取订单管理页面状态码: {order_manage_response.status_code}")
        
        # 从响应中提取CSRF令牌
        csrf_match = re.search(r'<input type="hidden" name="csrf_token" value="([^"\']+)"', order_manage_response.data.decode('utf-8'))
        if csrf_match:
            csrf_token = csrf_match.group(1)
            logger.info(f"从页面提取的CSRF令牌: {csrf_token}")
            
            # 尝试取消订单
            cancel_response = client.post(f'/admin/orders/{order_id}/cancel', data={
                'csrf_token': csrf_token
            })
        else:
            logger.error("无法从页面提取CSRF令牌")
            cancel_response = None
        
        if cancel_response:
            logger.info(f"取消订单状态码: {cancel_response.status_code}")
            logger.info(f"响应头: {dict(cancel_response.headers)}")
            logger.info(f"响应数据: {cancel_response.data.decode('utf-8')}")
        
        # 检查订单状态
        updated_order = Order.query.get(order_id)
        if updated_order:
            logger.info(f"更新后订单状态: {updated_order.status}")
    else:
        logger.error("没有找到可取消状态的订单")
