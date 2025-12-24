from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_required
from app import db
from app.models import Cart, CartItem, Product, Order, OrderItem, UserLog, Review
from app.forms import CheckoutForm, ReviewForm
from app.shop import shop
from app.email import send_order_confirmation
from datetime import datetime

@shop.route('/cart')
@login_required
def cart():
    """购物车页面"""
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()
    
    return render_template('cart.html', cart=cart)

@shop.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    """添加商品到购物车"""
    product = Product.query.get_or_404(product_id)
    quantity = request.form.get('quantity', 1, type=int)
    
    if quantity <= 0:
        flash('数量必须大于0', 'warning')
        return redirect(url_for('main.product_detail', id=product_id))
    
    if quantity > product.stock:
        flash('库存不足', 'danger')
        return redirect(url_for('main.product_detail', id=product_id))
    
    # 获取或创建购物车
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.flush()
    
    # 检查购物车中是否已有该商品
    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if cart_item:
        new_quantity = cart_item.quantity + quantity
        if new_quantity > product.stock:
            flash('库存不足', 'danger')
            return redirect(url_for('main.product_detail', id=product_id))
        cart_item.quantity = new_quantity
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    
    # 记录日志
    log = UserLog(
        user_id=current_user.id,
        action='add_to_cart',
        details=f'添加商品到购物车: {product.name} x{quantity}',
        ip_address=request.remote_addr
    )
    db.session.add(log)
    
    db.session.commit()
    
    flash(f'成功添加 {quantity} 件商品到购物车', 'success')
    
    # 如果是AJAX请求，返回JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'success': True,
            'message': f'成功添加 {quantity} 件商品到购物车',
            'cart_items_count': cart.get_items_count(),
            'cart_total_price': cart.get_total_price()
        })
    
    return redirect(url_for('shop.cart'))

@shop.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    """从购物车移除商品"""
    cart_item = CartItem.query.get_or_404(item_id)
    cart = cart_item.cart
    
    if cart.user_id != current_user.id:
        flash('无权操作', 'danger')
        return redirect(url_for('shop.cart'))
    
    product_name = cart_item.product.name
    quantity = cart_item.quantity
    
    db.session.delete(cart_item)
    
    # 记录日志
    log = UserLog(
        user_id=current_user.id,
        action='remove_from_cart',
        details=f'从购物车移除商品: {product_name} x{quantity}',
        ip_address=request.remote_addr
    )
    db.session.add(log)
    
    db.session.commit()
    
    flash(f'已从购物车移除 {product_name}', 'success')
    
    # 如果是AJAX请求，返回JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        return jsonify({
            'success': True,
            'message': f'已从购物车移除 {product_name}',
            'cart_items_count': cart.get_items_count() if cart else 0,
            'cart_total_price': cart.get_total_price() if cart else 0
        })
    
    return redirect(url_for('shop.cart'))

@shop.route('/cart/update', methods=['POST'])
@login_required
def update_cart():
    """更新购物车商品数量"""
    item_id = request.form.get('item_id', type=int)
    quantity = request.form.get('quantity', type=int)
    
    if not item_id or quantity is None:
        return jsonify({'success': False, 'message': '参数错误'})
    
    cart_item = CartItem.query.get_or_404(item_id)
    cart = cart_item.cart
    
    if cart.user_id != current_user.id:
        return jsonify({'success': False, 'message': '无权操作'})
    
    if quantity <= 0:
        # 删除商品
        db.session.delete(cart_item)
        action = 'remove'
    else:
        # 检查库存
        if quantity > cart_item.product.stock:
            return jsonify({'success': False, 'message': '库存不足'})
        
        cart_item.quantity = quantity
        action = 'update'
    
    # 记录日志
    log = UserLog(
        user_id=current_user.id,
        action=f'{action}_cart_item',
        details=f'更新购物车商品: {cart_item.product.name} -> {quantity}件',
        ip_address=request.remote_addr
    )
    db.session.add(log)
    
    db.session.commit()
    
    # 重新查询购物车
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    
    return jsonify({
        'success': True,
        'item_total': cart_item.get_subtotal() if quantity > 0 else 0,
        'cart_total': cart.get_total_price() if cart else 0,
        'cart_items_count': cart.get_items_count() if cart else 0
    })

@shop.route('/cart/clear', methods=['POST'])
@login_required
def clear_cart():
    """清空购物车"""
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    
    if cart:
        # 记录日志
        log = UserLog(
            user_id=current_user.id,
            action='clear_cart',
            details='清空购物车',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        
        # 删除所有购物车项
        for item in cart.items:
            db.session.delete(item)
        
        db.session.commit()
        flash('购物车已清空', 'success')
    
    return redirect(url_for('shop.cart'))

@shop.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """结算页面"""
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    
    # 检查购物车是否为空
    if not cart or cart.items.count() == 0:
        flash('购物车为空，请先添加商品', 'warning')
        return redirect(url_for('shop.cart'))
    
    # 检查库存
    out_of_stock_items = []
    for item in cart.items:
        if item.quantity > item.product.stock:
            out_of_stock_items.append({
                'name': item.product.name,
                'requested': item.quantity,
                'available': item.product.stock
            })
    
    if out_of_stock_items:
        for item in out_of_stock_items:
            flash(f'商品 "{item["name"]}" 库存不足，剩余 {item["available"]} 件', 'danger')
        return redirect(url_for('shop.cart'))
    
    form = CheckoutForm()
    
    # 预填充用户信息
    if not form.is_submitted():
        form.shipping_address.data = current_user.address
        form.phone.data = current_user.phone
    
    if form.validate_on_submit():
        try:
            # 生成订单号
            order = Order(
                user_id=current_user.id,
                shipping_address=form.shipping_address.data,
                phone=form.phone.data,
                notes=form.notes.data,
                status='pending'
            )
            order.order_number = order.generate_order_number()
            
            # 添加订单项
            total_amount = 0
            for cart_item in cart.items:
                order_item = OrderItem(
                    order=order,
                    product_id=cart_item.product_id,
                    product_name=cart_item.product.name,
                    product_price=cart_item.product.price,
                    quantity=cart_item.quantity
                )
                total_amount += order_item.get_subtotal()
                
                # 更新商品库存
                cart_item.product.stock -= cart_item.quantity
                db.session.add(order_item)
            
            order.total_amount = total_amount
            
            # 清空购物车
            for cart_item in cart.items:
                db.session.delete(cart_item)
            
            # 记录订单日志
            log = UserLog(
                user_id=current_user.id,
                action='checkout',
                details=f'下单: {order.order_number}，总金额: ¥{total_amount}',
                ip_address=request.remote_addr
            )
            db.session.add(log)
            
            db.session.add(order)
            db.session.commit()
            
            # 发送订单确认邮件
            try:
                send_order_confirmation(order, current_user)
            except Exception as e:
                # 邮件发送失败不影响订单创建
                pass
            
            flash('订单创建成功！我们将在24小时内处理您的订单。', 'success')
            return redirect(url_for('shop.order_detail', order_id=order.id))
            
        except Exception as e:
            db.session.rollback()
            flash('订单创建失败，请稍后重试', 'danger')
    
    return render_template('checkout.html', form=form, cart=cart)

@shop.route('/orders')
@login_required
def orders():
    """订单列表页面"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    
    query = Order.query.filter_by(user_id=current_user.id)
    
    if status:
        query = query.filter_by(status=status)
    
    orders = query.order_by(Order.created_at.desc())\
        .paginate(page=page, per_page=10, error_out=False)
    
    return render_template('orders.html', orders=orders, status=status)

@shop.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    """订单详情页面"""
    order = Order.query.get_or_404(order_id)
    
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('无权查看此订单', 'danger')
        return redirect(url_for('shop.orders'))
    
    return render_template('order_detail.html', order=order)

@shop.route('/order/<int:order_id>/cancel', methods=['POST'])
@login_required
def cancel_order(order_id):
    """取消订单"""
    order = Order.query.get_or_404(order_id)
    
    if order.user_id != current_user.id:
        flash('无权操作此订单', 'danger')
        return redirect(url_for('shop.orders'))
    
    if order.status not in ['pending', 'paid']:
        flash('该订单状态无法取消', 'warning')
        return redirect(url_for('shop.order_detail', order_id=order_id))
    
    try:
        order.status = 'cancelled'
        
        # 恢复商品库存
        for item in order.items:
            product = Product.query.get(item.product_id)
            if product:
                product.stock += item.quantity
        
        # 记录日志
        log = UserLog(
            user_id=current_user.id,
            action='cancel_order',
            details=f'取消订单: {order.order_number}',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        
        db.session.commit()
        flash('订单已取消', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('取消失败，请稍后重试', 'danger')
    
    return redirect(url_for('shop.order_detail', order_id=order_id))

@shop.route('/review/<int:product_id>', methods=['GET', 'POST'])
@login_required
def add_review(product_id):
    """添加商品评价"""
    product = Product.query.get_or_404(product_id)
    
    # 检查用户是否购买过该商品
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
