#!/usr/bin/env python3
"""
测试用户端取消订单功能
验证用户通过"我的订单"进入订单详情后，取消订单时不会出现400错误
"""

import requests
from bs4 import BeautifulSoup
import re

BASE_URL = 'http://127.0.0.1:5000'

# 用户登录信息
USERNAME = 'testuser'
PASSWORD = 'test123'

def get_csrf_token(response):
    """从响应中提取CSRF令牌"""
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
    return csrf_token

def test_user_cancel_order():
    """测试用户端取消订单功能"""
    print("=" * 60)
    print("测试用户端取消订单功能")
    print("=" * 60)
    
    # 创建会话
    session = requests.Session()
    
    # 1. 访问登录页面获取CSRF令牌
    login_page = session.get(f'{BASE_URL}/auth/login')
    csrf_token = get_csrf_token(login_page)
    print(f"✓ 获取CSRF令牌: {csrf_token[:20]}...")
    
    # 2. 用户登录
    login_data = {
        'username': USERNAME,
        'password': PASSWORD,
        'csrf_token': csrf_token
    }
    login_response = session.post(f'{BASE_URL}/auth/login', data=login_data)
    
    if 'dashboard' in login_response.url or 'index' in login_response.url:
        print("✓ 用户登录成功")
    else:
        print("✗ 用户登录失败")
        return False
    
    # 3. 访问订单列表
    order_list_page = session.get(f'{BASE_URL}/order/list')
    if order_list_page.status_code == 200:
        print("✓ 访问订单列表成功")
    else:
        print(f"✗ 访问订单列表失败，状态码: {order_list_page.status_code}")
        return False
    
    # 4. 查找第一个待处理的订单
    soup = BeautifulSoup(order_list_page.text, 'html.parser')
    order_cards = soup.find_all('div', class_='order-card')
    pending_order_link = None
    
    for card in order_cards:
        # 查找订单状态文本
        order_info = card.find('div', class_='order-info')
        if order_info and '订单状态: pending' in order_info.text:
            detail_link = card.find('a', text='查看详情')
            if detail_link:
                pending_order_link = detail_link['href']
                break
    
    if not pending_order_link:
        print("✗ 没有找到待处理的订单，请先创建一个订单")
        return False
    
    print(f"✓ 找到待处理订单: {pending_order_link}")
    
    # 5. 访问订单详情页面
    order_detail_page = session.get(f'{BASE_URL}{pending_order_link}')
    if order_detail_page.status_code == 200:
        print("✓ 访问订单详情成功")
    else:
        print(f"✗ 访问订单详情失败，状态码: {order_detail_page.status_code}")
        return False
    
    # 6. 提取取消订单表单的CSRF令牌
    soup = BeautifulSoup(order_detail_page.text, 'html.parser')
    cancel_form = soup.find('form')
    
    if not cancel_form:
        print("✗ 没有找到取消订单表单")
        return False
    
    # 检查表单是否有CSRF令牌
    csrf_input = cancel_form.find('input', {'name': 'csrf_token'})
    if csrf_input:
        csrf_token = csrf_input['value']
        print(f"✓ 找到取消订单表单的CSRF令牌: {csrf_token[:20]}...")
    else:
        print("✗ 取消订单表单缺少CSRF令牌")
        return False
    
    # 7. 提交取消订单请求
    cancel_url = cancel_form['action']
    cancel_data = {
        'csrf_token': csrf_token
    }
    
    print(f"✓ 提交取消订单请求: {cancel_url}")
    cancel_response = session.post(f'{BASE_URL}{cancel_url}', data=cancel_data)
    
    # 8. 检查响应
    if cancel_response.status_code == 200:
        print("✓ 取消订单请求成功，状态码: 200")
        
        # 检查订单状态是否已更新
        soup = BeautifulSoup(cancel_response.text, 'html.parser')
        status_badge = soup.find('div', class_='status-badge')
        
        if status_badge and 'cancelled' in status_badge.text:
            print("✓ 订单状态已更新为 'cancelled'")
            print("🎉 测试通过！用户端取消订单功能已修复")
            return True
        else:
            print("✗ 订单状态未更新为 'cancelled'")
            return False
    else:
        print(f"✗ 取消订单请求失败，状态码: {cancel_response.status_code}")
        print(f"  错误信息: {cancel_response.text[:500]}...")
        return False

if __name__ == '__main__':
    success = test_user_cancel_order()
    
    if success:
        print("\n" + "=" * 60)
        print("测试结果: 成功")
        print("修复验证: 用户端取消订单不再出现400错误")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("测试结果: 失败")
        print("修复验证: 用户端取消订单仍然出现问题")
        print("=" * 60)