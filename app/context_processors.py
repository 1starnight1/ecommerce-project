from datetime import datetime
from app.models import Category

def inject_now():
    """注入当前时间"""
    return {'now': datetime.utcnow()}

def inject_categories():
    """注入分类列表"""
    categories = Category.query.all()
    return {'categories': categories}

def inject_cart_info():
    """注入购物车信息"""
    from flask_login import current_user
    from app.models import Cart
    
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if cart:
            return {
                'cart_items_count': cart.get_items_count(),
                'cart_total_price': cart.get_total_price()
            }
    return {
        'cart_items_count': 0,
        'cart_total_price': 0
    }
