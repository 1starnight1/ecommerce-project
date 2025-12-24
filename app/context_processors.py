from datetime import datetime
from app.models import Category
from flask_login import current_user
from app.models import Cart, CartItem


def inject_now():
    """注入当前时间"""
    return {'now': datetime.utcnow()}


def inject_categories():
    """注入分类列表"""
    try:
        categories = Category.query.order_by(Category.name).all()
        return {'categories': categories}
    except:
        return {'categories': []}


def inject_cart_info():
    """注入购物车信息"""
    from flask_login import current_user

    cart_items_count = 0
    cart_total_amount = 0

    if current_user.is_authenticated:
        try:
            cart = Cart.query.filter_by(user_id=current_user.id).first()
            if cart:
                cart_items_count = cart.total_quantity
                cart_total_amount = float(cart.total_price)
        except:
            # 数据库可能还没有准备好
            pass

    return {
        'cart_items_count': cart_items_count,
        'cart_total_amount': cart_total_amount
    }