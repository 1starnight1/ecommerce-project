import unittest
from flask import url_for
from app import create_app, db
from app.models import User, Product, Cart, CartItem, Order, OrderItem

class TestCartOrder(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            
            # 创建测试用户，使用随机数确保用户名唯一
            import uuid
            self.username = f'testuser_{uuid.uuid4().hex[:8]}'
            self.email = f'{self.username}@example.com'
            self.user = User(username=self.username, email=self.email)
            self.user.set_password('password')
            db.session.add(self.user)
            
            # 创建测试产品
            self.product = Product(
                name='测试商品',
                description='这是一个测试商品',
                price=100.0,
                stock=10
            )
            db.session.add(self.product)
            
            db.session.commit()
            
            # 保存用户和产品的 ID
            self.user_id = self.user.id
            self.product_id = self.product.id
            
            # 登录用户
            self.client.post('/auth/login', data={
                'username': self.username,
                'password': 'password'
            })
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_add_to_cart(self):
        """测试添加商品到购物车"""
        with self.app.app_context():
            # 添加商品到购物车
            response = self.client.post(f'/cart/add/{self.product_id}', data={
                'quantity': 2
            })
            
            # 检查响应
            self.assertEqual(response.status_code, 302)
            
            # 检查购物车
            cart = Cart.query.filter_by(user_id=self.user_id).first()
            self.assertIsNotNone(cart)
            
            # 检查购物车商品
            cart_item = CartItem.query.filter_by(
                cart_id=cart.id,
                product_id=self.product_id
            ).first()
            self.assertIsNotNone(cart_item)
            self.assertEqual(cart_item.quantity, 2)
    
    def test_view_cart(self):
        """测试查看购物车"""
        with self.app.app_context():
            # 添加商品到购物车
            cart = Cart(user_id=self.user_id)
            db.session.add(cart)
            db.session.commit()
            
            # 获取产品对象
            product = Product.query.get(self.product_id)
            
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=self.product_id,
                quantity=3,
                price=product.price
            )
            db.session.add(cart_item)
            db.session.commit()
            
            # 查看购物车
            response = self.client.get('/cart/')
            self.assertEqual(response.status_code, 200)
            response_text = response.get_data(as_text=True)
            self.assertIn('测试商品', response_text)
            self.assertIn('3 件', response_text)
    
    def test_checkout(self):
        """测试结账功能"""
        with self.app.app_context():
            # 添加商品到购物车
            cart = Cart(user_id=self.user_id)
            db.session.add(cart)
            db.session.commit()
            
            # 获取产品对象
            product = Product.query.get(self.product_id)
            
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=self.product_id,
                quantity=2,
                price=product.price
            )
            db.session.add(cart_item)
            db.session.commit()
            
            # 结账
            response = self.client.post('/order/checkout', data={
                'shipping_address': '测试地址',
                'payment_method': 'alipay',
                'notes': '测试备注'
            })
            
            # 检查响应
            self.assertEqual(response.status_code, 302)
            
            # 检查订单
            order = Order.query.filter_by(user_id=self.user_id).first()
            self.assertIsNotNone(order)
            self.assertEqual(order.shipping_address, '测试地址')
            self.assertEqual(order.payment_method, 'alipay')
            self.assertEqual(order.notes, '测试备注')
            
            # 检查订单项
            order_item = OrderItem.query.filter_by(order_id=order.id).first()
            self.assertIsNotNone(order_item)
            self.assertEqual(order_item.product_id, self.product_id)
            self.assertEqual(order_item.quantity, 2)
            
            # 检查购物车是否清空
            cart = Cart.query.filter_by(user_id=self.user_id).first()
            self.assertEqual(cart.items.count(), 0)
    
    def test_order_list(self):
        """测试订单列表"""
        with self.app.app_context():
            # 创建测试订单
            order = Order(
                order_number='TEST123',
                user_id=self.user_id,
                total_amount=200.0,
                shipping_address='测试地址',
                payment_method='alipay',
                status='pending'
            )
            db.session.add(order)
            db.session.commit()
            
            # 查看订单列表
            response = self.client.get('/order/list')
            self.assertEqual(response.status_code, 200)
            response_text = response.get_data(as_text=True)
            self.assertIn('TEST123', response_text)
    
    def test_order_detail(self):
        """测试订单详情"""
        with self.app.app_context():
            # 创建测试订单
            order = Order(
                order_number='TEST456',
                user_id=self.user_id,
                total_amount=300.0,
                shipping_address='测试地址',
                payment_method='wechat',
                status='pending'
            )
            db.session.add(order)
            db.session.commit()
            
            # 查看订单详情
            response = self.client.get(f'/order/{order.id}')
            self.assertEqual(response.status_code, 200)
            response_text = response.get_data(as_text=True)
            self.assertIn('TEST456', response_text)
            self.assertIn('测试地址', response_text)

if __name__ == '__main__':
    unittest.main()