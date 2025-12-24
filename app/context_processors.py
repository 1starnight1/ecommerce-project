from datetime import datetime
from app.models import Category

def inject_now():
    """注入当前时间"""
    return {'now': datetime.utcnow()}

def inject_categories():
    """注入分类列表"""
    try:
        categories = Category.query.all()
        return {'categories': categories}
    except:
        # 如果数据库还没初始化，返回空列表
        return {'categories': []}

def inject_cart_info():
    """注入购物车信息"""
    from flask_login import current_user
    from app.models import Cart, CartItem
    
    cart_items_count = 0
    
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if cart:
            cart_items_count = sum(item.quantity for item in cart.items)
    
    return {
        'cart_items_count': cart_items_count
    }
