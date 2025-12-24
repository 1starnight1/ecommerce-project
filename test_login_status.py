# test_login_status.py
import requests
from bs4 import BeautifulSoup


def test_login():
    print("=== 测试登录状态 ===")

    # 1. 访问首页
    print("\n1. 访问首页...")
    response = requests.get('http://127.0.0.1:5000/')
    print(f"   状态码: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title')
    if title:
        print(f"   页面标题: {title.text}")

    # 2. 尝试登录
    print("\n2. 尝试登录...")
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }

    # 先获取登录页面的cookie
    session = requests.Session()
    login_page = session.get('http://127.0.0.1:5000/auth/login')

    # 提交登录表单
    login_response = session.post('http://127.0.0.1:5000/auth/login', data=login_data)
    print(f"   登录状态码: {login_response.status_code}")

    # 3. 登录后访问首页
    print("\n3. 登录后访问首页...")
    home_response = session.get('http://127.0.0.1:5000/')
    print(f"   状态码: {home_response.status_code}")

    # 检查是否显示用户名
    home_soup = BeautifulSoup(home_response.text, 'html.parser')
    h1_tags = home_soup.find_all('h1')
    for h1 in h1_tags:
        if '欢迎' in h1.text:
            print(f"   欢迎信息: {h1.text}")

    # 4. 测试登出
    print("\n4. 测试登出...")
    logout_response = session.get('http://127.0.0.1:5000/auth/logout')
    print(f"   登出状态码: {logout_response.status_code}")


if __name__ == "__main__":
    test_login()