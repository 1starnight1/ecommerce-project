from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app import db
from app.models import Product, Category, Order, User, UserLog
from app.forms import ProductForm, CategoryForm
from app.admin import admin


@admin.before_request
def check_admin():
    if not current_user.is_authenticated or not current_user.is_admin:
        flash('需要管理员权限', 'danger')
        return redirect(url_for('main.index'))


@admin.route('/dashboard')
@login_required
def dashboard():
    # 统计信息
    total_orders = Order.query.count()
    total_users = User.query.count()
    total_products = Product.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0

    # 最近订单
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()

    # 销售统计（按天）
    from datetime import datetime, timedelta
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30)

    return render_template('admin/dashboard.html',
                           total_orders=total_orders,
                           total_users=total_users,
                           total_products=total_products,
                           total_revenue=total_revenue,
                           recent_orders=recent_orders)


@admin.route('/products')
@login_required
def product_manage():
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category_id', type=int)

    query = Product.query
    if category_id:
        query = query.filter_by(category_id=category_id)

    products = query.order_by(Product.created_at.desc()) \
        .paginate(page=page, per_page=20, error_out=False)

    categories = Category.query.all()

    return render_template('admin/product_manage.html',
                           products=products,
                           categories=categories,
                           category_id=category_id)


@admin.route('/product/add', methods=['GET', 'POST'])
@login_required
def product_add():
    form = ProductForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data,
            category_id=form.category_id.data
        )

        db.session.add(product)
        db.session.commit()

        flash('商品添加成功', 'success')
        return redirect(url_for('admin.product_manage'))

    return render_template('admin/product_edit.html', form=form, title='添加商品')


@admin.route('/product/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def product_edit(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.stock = form.stock.data
        product.category_id = form.category_id.data

        db.session.commit()
        flash('商品更新成功', 'success')
        return redirect(url_for('admin.product_manage'))

    return render_template('admin/product_edit.html', form=form, title='编辑商品')


@admin.route('/product/delete/<int:id>', methods=['POST'])
@login_required
def product_delete(id):
    product = Product.query.get_or_404(id)

    db.session.delete(product)
    db.session.commit()

    flash('商品删除成功', 'success')
    return redirect(url_for('admin.product_manage'))


@admin.route('/categories')
@login_required
def category_manage():
    categories = Category.query.all()
    return render_template('admin/category_manage.html', categories=categories)


@admin.route('/category/add', methods=['GET', 'POST'])
@login_required
def category_add():
    form = CategoryForm()

    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            description=form.description.data
        )

        db.session.add(category)
        db.session.commit()

        flash('分类添加成功', 'success')
        return redirect(url_for('admin.category_manage'))

    return render_template('admin/category_edit.html', form=form, title='添加分类')


@admin.route('/orders')
@login_required
def order_manage():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')

    query = Order.query
    if status:
        query = query.filter_by(status=status)

    orders = query.order_by(Order.created_at.desc()) \
        .paginate(page=page, per_page=20, error_out=False)

    return render_template('admin/order_manage.html', orders=orders, status=status)


@admin.route('/order/<int:id>')
@login_required
def order_view(id):
    order = Order.query.get_or_404(id)
    return render_template('admin/order_view.html', order=order)


@admin.route('/order/update_status/<int:id>', methods=['POST'])
@login_required
def order_update_status(id):
    order = Order.query.get_or_404(id)
    status = request.form.get('status')

    if status in ['pending', 'paid', 'shipped', 'delivered', 'cancelled']:
        order.status = status
        db.session.commit()
        flash('订单状态已更新', 'success')

    return redirect(url_for('admin.order_view', id=id))


@admin.route('/users')
@login_required
def user_manage():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.created_at.desc()) \
        .paginate(page=page, per_page=20, error_out=False)

    return render_template('admin/user_manage.html', users=users)


@admin.route('/logs')
@login_required
def user_logs():
    page = request.args.get('page', 1, type=int)
    user_id = request.args.get('user_id', type=int)

    query = UserLog.query
    if user_id:
        query = query.filter_by(user_id=user_id)

    logs = query.order_by(UserLog.created_at.desc()) \
        .paginate(page=page, per_page=50, error_out=False)

    return render_template('admin/user_logs.html', logs=logs)