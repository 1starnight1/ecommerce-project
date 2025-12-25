from flask import current_app, Flask
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath('.'))

# 导入应用
from app import create_app
from app.models import db, User

# 创建应用实例
app = create_app()

with app.app_context():
    # 检查是否有测试用户，如果没有则创建一个
    test_user = User.query.filter_by(email='test@example.com').first()
    if not test_user:
        test_user = User(username='testuser', email='test@example.com', password='password123')
        db.session.add(test_user)
        db.session.commit()
        print("创建了测试用户: test@example.com / password123")

# 使用测试客户端进行测试
with app.test_client() as client:
    # 登录测试用户
    login_response = client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    
    print(f"登录状态码: {login_response.status_code}")
    
    # 访问订单页面
    orders_response = client.get('/shop/orders', follow_redirects=True)
    
    print(f"订单页面状态码: {orders_response.status_code}")
    
    if orders_response.status_code == 200:
        print("✅ 订单页面访问成功!")
        print("页面内容前500字符:")
        print(orders_response.data.decode('utf-8')[:500])
        
        # 检查是否有数据库相关错误
        if 'sqlalchemy.exc' in orders_response.data.decode('utf-8'):
            print("❌ 页面中包含SQLAlchemy错误!")
        elif 'no such column' in orders_response.data.decode('utf-8'):
            print("❌ 页面中包含'column not found'错误!")
        else:
            print("✅ 页面中没有明显的数据库错误!")
    else:
        print(f"❌ 订单页面访问失败，状态码: {orders_response.status_code}")
        print("响应内容:")
        print(orders_response.data.decode('utf-8'))
