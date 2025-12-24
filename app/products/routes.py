"""
商品模块路由
"""
from flask import Blueprint, render_template, request, flash
from flask_login import current_user
from .. import db
from ..models import Product
from ..utils import log_user_action

products_bp = Blueprint('products', __name__, url_prefix='/products')

@products_bp.route('/')
def list_products():
    """商品列表"""
    category = request.args.get('category')
    search = request.args.get('search', '').strip()
    
    # 构建查询
    query = Product.query
    
    # 分类筛选
    if category:
        query = query.filter_by(category=category)
    
    # 搜索
    if search:
        query = query.filter(
            db.or_(
                Product.name.contains(search),
                Product.description.contains(search)
            )
        )
    
    # 排序
    query = query.order_by(Product.created_at.desc())
    
    products = query.all()
    
    # 记录搜索日志
    if current_user.is_authenticated and search:
        log_user_action(current_user.id, 'search', details=f"search: {search}")
    
    # 记录浏览日志
    if current_user.is_authenticated and not search:
        for product in products:
            log_user_action(current_user.id, 'view', product.id)
    
    return render_template('products/list.html',
                         products=products,
                         category=category,
                         search=search)

@products_bp.route('/<int:product_id>')
def product_detail(product_id):
    """商品详情"""
    product = Product.query.get_or_404(product_id)
    
    # 记录浏览日志
    if current_user.is_authenticated:
        log_user_action(current_user.id, 'view_detail', product.id)
    
    # 获取相关商品（同一分类）
    related_products = Product.query.filter(
        Product.category == product.category,
        Product.id != product.id
    ).limit(4).all()
    
    return render_template('products/detail.html',
                         product=product,
                         related_products=related_products)
