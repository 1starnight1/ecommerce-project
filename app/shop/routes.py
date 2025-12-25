from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app import db
from app.models import Product, UserLog, Review, Order
from app.forms import ReviewForm
from app.shop import shop
from datetime import datetime

@shop.route('/review/<int:product_id>', methods=['GET', 'POST'])
@login_required
def add_review(product_id):
    """添加商品评价"""
    product = Product.query.get_or_404(product_id)
    
    # 检查用户是否购买过该商品
    from app.models import Order, OrderItem
    has_purchased = OrderItem.query\
        .join(Order)\
        .filter(Order.user_id == current_user.id)\
        .filter(OrderItem.product_id == product_id)\
        .filter(Order.status == 'delivered')\
        .first() is not None
    
    if not has_purchased:
        flash('只有购买过该商品并收到货的用户才能评价', 'warning')
        return redirect(url_for('main.product_detail', id=product_id))
    
    # 检查是否已评价过
    existing_review = Review.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()
    
    form = ReviewForm()
    
    if existing_review:
        form.rating.data = existing_review.rating
        form.comment.data = existing_review.comment
    
    if form.validate_on_submit():
        try:
            if existing_review:
                # 更新现有评价
                existing_review.rating = form.rating.data
                existing_review.comment = form.comment.data
                action = 'update'
            else:
                # 创建新评价
                review = Review(
                    user_id=current_user.id,
                    product_id=product_id,
                    rating=form.rating.data,
                    comment=form.comment.data
                )
                db.session.add(review)
                action = 'add'
            
            # 记录日志
            log = UserLog(
                user_id=current_user.id,
                action=f'{action}_review',
                details=f'{action}评价: {product.name}，评分: {form.rating.data}',
                ip_address=request.remote_addr
            )
            db.session.add(log)
            
            db.session.commit()
            flash('评价提交成功', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash('提交失败，请稍后重试', 'danger')
        
        return redirect(url_for('main.product_detail', id=product_id))
    
    return render_template('add_review.html', form=form, product=product, existing_review=existing_review)


