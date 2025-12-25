from app import create_app
import unittest

class TestCancelOrder(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False  # 测试时禁用CSRF保护
        self.client = self.app.test_client()
        
        # 创建测试上下文
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        self.app_context.pop()
    
    def test_cancel_order_route_exists(self):
        """测试取消订单路由是否存在"""
        with self.client as client:
            # 测试GET请求应该返回405（方法不允许）
            response = client.get('/admin/orders/1/cancel')
            print(f"GET请求状态码: {response.status_code}")
            
            # 测试POST请求
            response = client.post('/admin/orders/1/cancel')
            print(f"POST请求状态码: {response.status_code}")
            print(f"响应内容: {response.data.decode('utf-8')}")
            print(f"响应头: {dict(response.headers)}")

if __name__ == '__main__':
    unittest.main(verbosity=2)
