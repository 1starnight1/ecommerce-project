# app/models.py
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    """用户模型"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    # 用户信息
    phone = db.Column(db.String(20))
    address = db.Column(db.String(500))
    avatar = db.Column(db.String(200), default='default_avatar.png')

    # 关系
    orders = db.relationship('Order', backref='user', lazy='dynamic')
    cart_items = db.relationship('CartItem', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    logs = db.relationship('UserLog', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_cart_total(self):
        """计算购物车总价"""
        total = 0
        for item in self.cart_items:
            total += item.quantity * item.product.price
        return total

    def get_cart_count(self):
        """计算购物车商品数量"""
        return sum(item.quantity for item in self.cart_items)

    def __repr__(self):
        return f'<User {self.username}>'


class Product(db.Model):
    """商品模型"""
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    category = db.Column(db.String(50))
    image = db.Column(db.String(200), default='default_product.png')
    sku = db.Column(db.String(50), unique=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关系
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic')
    cart_items = db.relationship('CartItem', backref='product', lazy='dynamic')

    def __repr__(self):
        return f'<Product {self.name}>'


class Order(db.Model):
    """订单模型"""
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, paid, shipped, completed, cancelled
    shipping_address = db.Column(db.String(500))
    payment_method = db.Column(db.String(50))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    paid_at = db.Column(db.DateTime)
    shipped_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)

    # 关系
    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')

    def generate_order_number(self):
        """生成订单号"""
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f'ORD{timestamp}{self.user_id:04d}'

    def get_status_text(self):
        """获取订单状态文本"""
        status_map = {
            'pending': '待支付',
            'paid': '已支付',
            'shipped': '已发货',
            'completed': '已完成',
            'cancelled': '已取消'
        }
        return status_map.get(self.status, self.status)

    def get_status_color(self):
        """获取订单状态颜色"""
        color_map = {
            'pending': 'warning',
            'paid': 'info',
            'shipped': 'primary',
            'completed': 'success',
            'cancelled': 'danger'
        }
        return color_map.get(self.status, 'secondary')

    def __repr__(self):
        return f'<Order {self.order_number}>'


class OrderItem(db.Model):
    """订单商品项"""
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  # 购买时的价格
    subtotal = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<OrderItem {self.id}>'


class CartItem(db.Model):
    """购物车商品项"""
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<CartItem {self.id}>'


class UserLog(db.Model):
    """用户操作日志"""
    __tablename__ = 'user_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<UserLog {self.user_id} - {self.action}>'