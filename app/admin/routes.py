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
    total_orders = Order.query.filter_by(status='pending').count()
    total_users = User.query.count()
    total_products = Product.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).filter_by(status='pending').scalar() or 0
    
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


@admin.route('/products/add', methods=['GET', 'POST'])
@admin_required
def add_product():
    """添加商品"""
    form = ProductForm()
    # 动态加载分类选项
    form.category_id.choices = [(category.id, category.name) for category in Category.query.order_by(Category.name)]
    
    if form.validate_on_submit():
        # 创建新商品
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data,
            category_id=form.category_id.data
        )
        db.session.add(product)
        db.session.commit()
        
        # 重定向到商品管理页面
        return redirect(url_for('admin.product_manage'))
    
    return render_template('add_product.html', form=form)


@admin.route('/products/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_product(id):
    """编辑商品"""
    # 获取要编辑的商品
    product = Product.query.get_or_404(id)
    
    form = ProductForm(obj=product)  # 使用现有商品数据初始化表单
    # 动态加载分类选项
    form.category_id.choices = [(category.id, category.name) for category in Category.query.order_by(Category.name)]
    
    if form.validate_on_submit():
        # 更新商品信息
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.stock = form.stock.data
        product.category_id = form.category_id.data
        
        db.session.commit()
        
        # 重定向到商品管理页面
        return redirect(url_for('admin.product_manage'))
    
    return render_template('edit_product.html', form=form, product=product)


@admin.route('/products/delete/<int:id>', methods=['POST'])
@admin_required
def delete_product(id):
    """删除商品"""
    # 获取要删除的商品
    product = Product.query.get_or_404(id)
    
    # 删除商品
    db.session.delete(product)
    db.session.commit()
    
    # 重定向到商品管理页面
    return redirect(url_for('admin.product_manage'))

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


@admin.route('/orders/<int:id>')
@admin_required
def order_detail(id):
    """订单详情"""
    order = Order.query.get_or_404(id)
    return render_template('order_detail.html', order=order)


@admin.route('/orders/<int:id>/cancel', methods=['POST'])
@admin_required
def cancel_order(id):
    """取消订单"""
    import logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    # 记录请求信息
    logger.debug(f"取消订单请求: ID={id}, 用户={current_user.username if current_user.is_authenticated else '未登录'}")
    logger.debug(f"请求方法: {request.method}")
    logger.debug(f"请求数据: {request.form}")
    logger.debug(f"请求头: {dict(request.headers)}")
    
    try:
        order = Order.query.get_or_404(id)
        logger.debug(f"找到订单: ID={order.id}, 状态={order.status}")
        
        # 只有pending或paid状态的订单才能取消
        if order.status not in ['pending', 'paid']:
            flash('该订单状态不允许取消', 'danger')
            logger.debug(f"订单状态不允许取消: {order.status}")
            return redirect(url_for('admin.order_manage'))
        
        # 恢复库存
        for item in order.items:
            product = Product.query.get(item.product_id)
            if product:
                product.stock += item.quantity
                logger.debug(f"恢复商品库存: 商品ID={item.product_id}, 数量={item.quantity}, 恢复后库存={product.stock}")
        
        # 更新订单状态为取消
        order.status = 'cancelled'
        logger.debug(f"更新订单状态为: cancelled")
        db.session.commit()
        logger.debug(f"订单状态更新成功")
        
        flash('订单已成功取消', 'success')
        return redirect(url_for('admin.order_manage'))
    except Exception as e:
        logger.error(f"取消订单失败: {str(e)}")
        db.session.rollback()
        flash(f'取消订单失败: {str(e)}', 'danger')
        return redirect(url_for('admin.order_manage'))


@admin.route('/orders/<int:id>/delete', methods=['POST'])
@admin_required
def delete_order(id):
    """删除已取消的订单"""
    import logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    # 记录请求信息
    logger.debug(f"删除订单请求: ID={id}, 用户={current_user.username if current_user.is_authenticated else '未登录'}")
    
    try:
        order = Order.query.get_or_404(id)
        logger.debug(f"找到订单: ID={order.id}, 状态={order.status}")
        
        # 只有已取消的订单才能删除
        if order.status != 'cancelled':
            flash('只有已取消的订单才能被删除', 'danger')
            logger.debug(f"订单状态不允许删除: {order.status}")
            return redirect(url_for('admin.order_manage'))
        
        # 删除订单
        db.session.delete(order)
        logger.debug(f"删除订单ID: {order.id}")
        db.session.commit()
        logger.debug(f"订单删除成功")
        
        flash('订单已成功删除', 'success')
        return redirect(url_for('admin.order_manage'))
    except Exception as e:
        logger.error(f"删除订单失败: {str(e)}")
        db.session.rollback()
        flash(f'删除订单失败: {str(e)}', 'danger')
        return redirect(url_for('admin.order_manage'))

@admin.route('/users')
@admin_required
def user_manage():
    """用户管理"""
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.created_at.desc())\
        .paginate(page=page, per_page=20, error_out=False)
    
    return render_template('user_manage.html', users=users)


@admin.route('/users/<int:id>')
@admin_required
def user_detail(id):
    """用户详情"""
    user = User.query.get_or_404(id)
    # 获取排序后的订单和日志
    orders = user.orders.order_by(Order.created_at.desc()).limit(10).all()
    logs = user.logs.order_by(UserLog.created_at.desc()).limit(10).all()
    return render_template('user_detail.html', user=user, orders=orders, logs=logs)

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
