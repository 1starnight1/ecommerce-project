from flask import render_template, redirect, url_for, flash, request, jsonify, abort
from flask_login import current_user, login_required
from app import db
from app.models import Product, Category, Order, User, UserLog
from app.forms import ProductForm, CategoryForm
from app.admin import admin

def admin_required(f):
    """管理员权限装饰器"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@admin.before_request
@login_required
def check_admin():
    """检查管理员权限"""
    if not current_user.is_admin:
        abort(403)

@admin.route('/dashboard')
@admin_required
def dashboard():
    """管理员仪表板"""
    # 基础统计
    total_orders = Order.query.count()
    total_users = User.query.count()
    total_products = Product.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
    
    # 最近订单
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html',
                         total_orders=total_orders,
                         total_users=total_users,
                         total_products=total_products,
                         total_revenue=total_revenue,
                         recent_orders=recent_orders)

@admin.route('/products')
@admin_required
def product_manage():
    """商品管理"""
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category_id', type=int)
    
    query = Product.query
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    query = query.order_by(Product.created_at.desc())
    
    products = query.paginate(page=page, per_page=20, error_out=False)
    
    categories = Category.query.all()
    
    return render_template('product_manage.html',
                         products=products,
                         categories=categories,
                         category_id=category_id)

@admin.route('/orders')
@admin_required
def order_manage():
    """订单管理"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    
    query = Order.query
    
    if status:
        query = query.filter_by(status=status)
    
    orders = query.order_by(Order.created_at.desc())\
        .paginate(page=page, per_page=20, error_out=False)
    
    return render_template('order_manage.html', orders=orders, status=status)

@admin.route('/users')
@admin_required
def user_manage():
    """用户管理"""
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.created_at.desc())\
        .paginate(page=page, per_page=20, error_out=False)
    
    return render_template('user_manage.html', users=users)

@admin.route('/logs')
@admin_required
def user_logs():
    """用户日志"""
    page = request.args.get('page', 1, type=int)
    user_id = request.args.get('user_id', type=int)
    
    query = UserLog.query
    
    if user_id:
        query = query.filter_by(user_id=user_id)
    
    logs = query.order_by(UserLog.created_at.desc())\
        .paginate(page=page, per_page=50, error_out=False)
    
    return render_template('user_logs.html', logs=logs)
