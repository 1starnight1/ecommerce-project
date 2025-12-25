import requests

# 测试路由列表
test_routes = [
    ('GET', 'http://127.0.0.1:5000/', '首页'),
    ('GET', 'http://127.0.0.1:5000/auth/login', '登录页面'),
    ('GET', 'http://127.0.0.1:5000/auth/register', '注册页面'),
    ('GET', 'http://127.0.0.1:5000/shop/cart', '购物车页面'),
    ('GET', 'http://127.0.0.1:5000/shop/orders', '订单页面'),
    ('GET', 'http://127.0.0.1:5000/shop/checkout', '结算页面'),
]

print("测试电商平台路由...")
print("=" * 60)

success_count = 0
failure_count = 0

for method, url, description in test_routes:
    try:
        if method == 'GET':
            response = requests.get(url, allow_redirects=True)
        else:
            response = requests.post(url, allow_redirects=True)
        
        if response.status_code in [200, 302, 301]:
            print(f"✓ {description} ({url}): {response.status_code}")
            success_count += 1
        else:
            print(f"✗ {description} ({url}): {response.status_code}")
            failure_count += 1
    except Exception as e:
        print(f"✗ {description} ({url}): 连接失败 - {e}")
        failure_count += 1

print("=" * 60)
print(f"测试完成: {success_count} 成功, {failure_count} 失败")
