import requests

try:
    response = requests.get('http://127.0.0.1:5000/shop/orders')
    print(f"HTTP状态码: {response.status_code}")
    if response.status_code == 200:
        print("页面访问成功!")
        print("页面内容前200字符:")
        print(response.text[:200])
    else:
        print(f"页面访问失败，状态码: {response.status_code}")
        print("错误信息:")
        print(response.text)
except Exception as e:
    print(f"请求失败: {e}")
