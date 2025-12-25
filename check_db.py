from app import create_app, db
from app.models import Order, User

# 创建Flask应用实例
app = create_app()

with app.app_context():
    print('订单数量:', Order.query.count())
    print('用户数量:', User.query.count())
    print('订单列表:', Order.query.limit(5).all())
    print('用户列表:', User.query.limit(5).all())
