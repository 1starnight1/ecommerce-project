from flask import render_template, request, flash
from flask_login import current_user, login_required
from app import db
from app.models import Product, Category, UserLog
from app.main import main


@main.route('/')
@main.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category_id', type=int)

    query = Product.query
    if category_id:
        query = query.filter_by(category_id=category_id)

    products = query.paginate(page=page, per_page=12, error_out=False)
    categories = Category.query.all()

    # 记录用户浏览日志
    if current_user.is_authenticated:
        log = UserLog(
            user_id=current_user.id,
            action='view_homepage',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()

    return render_template('main/index.html',
                           products=products,
                           categories=categories,
                           category_id=category_id)


@main.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)

    # 记录用户浏览商品日志
    if current_user.is_authenticated:
        log = UserLog(
            user_id=current_user.id,
            action='view_product',
            details=f'浏览商品: {product.name}',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()

    return render_template('main/product_detail.html', product=product)


@main.route('/search')
def search():
    keyword = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)

    if keyword:
        products = Product.query.filter(
            Product.name.contains(keyword) |
            Product.description.contains(keyword)
        ).paginate(page=page, per_page=12, error_out=False)
    else:
        products = Product.query.paginate(page=page, per_page=12, error_out=False)

    return render_template('main/search.html', products=products, keyword=keyword)