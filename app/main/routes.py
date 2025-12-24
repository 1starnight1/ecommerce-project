from flask import render_template, request, flash, jsonify
from flask_login import current_user, login_required
from app import db
from app.models import Product, Category, UserLog
from app.main import main
from sqlalchemy import or_

@main.route('/')
@main.route('/index')
def index():
    """首页"""
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category_id', type=int)
    sort_by = request.args.get('sort', 'newest')
    
    # 构建查询
    query = Product.query
    
    # 按分类过滤
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    # 排序
    if sort_by == 'price_low':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price_high':
        query = query.order_by(Product.price.desc())
    elif sort_by == 'popular':
        # 按销量排序（需要关联订单项统计）
        from sqlalchemy import func
        from app.models import OrderItem
        
        query = query.outerjoin(OrderItem)\
            .group_by(Product.id)\
            .order_by(func.sum(OrderItem.quantity).desc())
    else:  # newest
        query = query.order_by(Product.created_at.desc())
    
    # 分页
    per_page = 12
    products = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # 获取所有分类
    categories = Category.query.all()
    
    # 记录用户浏览日志
    if current_user.is_authenticated:
        log = UserLog(
            user_id=current_user.id,
            action='view_homepage',
            ip_address=request.remote_addr,
            details=f'浏览首页，分类: {category_id or "全部"}'
        )
        db.session.add(log)
        db.session.commit()
    
    return render_template('index.html', 
                         products=products, 
                         categories=categories,
                         category_id=category_id,
                         sort_by=sort_by)

@main.route('/product/<int:id>')
def product_detail(id):
    """商品详情页"""
    product = Product.query.get_or_404(id)
    
    # 获取相关商品（同分类）
    related_products = Product.query\
        .filter_by(category_id=product.category_id)\
        .filter(Product.id != product.id)\
        .order_by(db.func.random())\
        .limit(4)\
        .all()
    
    # 获取商品评价
    reviews = product.reviews.order_by(db.desc('created_at')).limit(10).all()
    
    # 计算平均评分
    from sqlalchemy import func
    avg_rating = db.session.query(func.avg('rating')).filter_by(product_id=id).scalar()
    
    # 记录用户浏览商品日志
    if current_user.is_authenticated:
        log = UserLog(
            user_id=current_user.id,
            action='view_product',
            details=f'浏览商品: {product.name} (ID: {product.id})',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
    
    return render_template('product_detail.html', 
                         product=product,
                         related_products=related_products,
                         reviews=reviews,
                         avg_rating=avg_rating)

@main.route('/search')
def search():
    """搜索页面"""
    keyword = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category_id', type=int)
    
    if not keyword:
        flash('请输入搜索关键词', 'warning')
        return redirect(url_for('main.index'))
    
    # 构建搜索查询
    query = Product.query.filter(
        or_(
            Product.name.contains(keyword),
            Product.description.contains(keyword)
        )
    )
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    # 分页
    per_page = 12
    products = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # 获取所有分类
    categories = Category.query.all()
    
    # 记录搜索日志
    if current_user.is_authenticated:
        log = UserLog(
            user_id=current_user.id,
            action='search',
            details=f'搜索关键词: {keyword}',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
    
    return render_template('search.html', 
                         products=products, 
                         keyword=keyword,
                         categories=categories,
                         category_id=category_id)

@main.route('/about')
def about():
    """关于我们页面"""
    return render_template('about.html')

@main.route('/contact')
def contact():
    """联系我们页面"""
    return render_template('contact.html')

@main.route('/api/products')
def api_products():
    """商品API（用于AJAX加载）"""
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category_id', type=int)
    
    query = Product.query
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    products = query.order_by(Product.created_at.desc())\
        .paginate(page=page, per_page=12, error_out=False)
    
    # 转换为字典列表
    products_data = [{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'image': p.image,
        'category': p.category.name if p.category else '',
        'stock': p.stock
    } for p in products.items]
    
    return jsonify({
        'products': products_data,
        'has_next': products.has_next,
        'next_num': products.next_num
    })
