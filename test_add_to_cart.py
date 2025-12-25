from app import create_app, db
from app.models import User, Product
from flask import url_for
import requests

# 创建测试客户端
app = create_app()
with app.test_client() as client:
    # 创建测试数据
    with app.app_context():
        # 创建测试用户
        test_user = User(username='testuser', email='test@example.com', phone='13900139000', address='测试地址', is_active=True)
        test_user.set_password('test123')
        db.session.add(test_user)
        
        # 创建测试商品
        test_product = Product(name='测试商品', description='测试商品描述', price=100.0, stock=10, category_id=None)
        db.session.add(test_product)
        db.session.commit()
    
    print("开始测试...")
    
    # 登录用户
    login_response = client.post('/auth/login', data={'username': 'testuser', 'password': 'test123'}, follow_redirects=True)
    print(f"登录状态: {'成功' if '登录成功' in login_response.data.decode() else '失败'}")
    
    # 获取首页并提取CSRF token
    index_response = client.get('/')
    csrf_token = index_response.data.decode().split('name="csrf_token" value="')[1].split('"')[0]
    
    # 测试添加商品到购物车
    add_to_cart_response = client.post(
        f'/cart/add/{test_product.id}', 
        data={'csrf_token': csrf_token, 'quantity': 1}, 
        follow_redirects=True
    )
    
    response_data = add_to_cart_response.data.decode()
    if '已添加' in response_data:
        print("添加商品到购物车成功！")
        print("404错误已修复！")
    else:
        print("添加商品到购物车失败！")
        print(f"响应状态码: {add_to_cart_response.status_code}")
        print(f"响应内容: {response_data}")
