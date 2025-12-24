import random
import string
from datetime import datetime
from flask import request
from .models import db, UserLog

def generate_order_number():
    """生成订单号"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_str = ''.join(random.choices(string.digits, k=6))
    return f'ORD{timestamp}{random_str}'

def log_user_action(user_id, action, product_id=None, details=""):
    """记录用户行为日志"""
    log = UserLog(
        user_id=user_id,
        action=action,
        product_id=product_id,
        details=details,
        ip_address=request.remote_addr if request else None,
        user_agent=request.user_agent.string if request and request.user_agent else None
    )
    db.session.add(log)
    db.session.commit()

def format_price(price):
    """格式化价格"""
    return f'¥{price:.2f}'

def calculate_cart_total(cart_items):
    """计算购物车总价"""
    return sum(item.product.price * item.quantity for item in cart_items)

def send_order_confirmation_email(user_email, order_number, order_details):
    """发送订单确认邮件（模拟函数）"""
    # 在实际应用中，这里应该集成邮件发送服务
    # 例如：使用 Flask-Mail 或 SMTP 服务
    print(f"[邮件发送] 发送订单确认邮件给: {user_email}")
    print(f"[邮件发送] 订单号: {order_number}")
    print(f"[邮件发送] 订单详情: {order_details}")
    print("[邮件发送] 邮件已发送（模拟）")
    return True
