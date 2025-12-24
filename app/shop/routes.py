from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_required
from app import db
from app.models import Cart, CartItem, Product, Order, OrderItem, UserLog
from app.forms import CheckoutForm, ReviewForm
from app.shop import shop


@shop.route('/cart')
@login_required
def cart():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()

    return render_template('shop/cart.html', cart=cart)


@shop.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = request.form.get('quantity', 1, type=int)

    if quantity > product.stock:
        flash('库存不足', 'danger')
        return redirect(url_for('main.product_detail', id=product_id))

    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()

    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
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

    flash('商品已添加到购物车', 'success')
    return redirect(url_for('shop.cart'))


@shop.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)

    if cart_item.cart.user_id != current_user.id:
        flash('无权操作', 'danger')
        return redirect(url_for('shop.cart'))

    db.session.delete(cart_item)
    db.session.commit()

    flash('商品已从购物车移除', 'success')
    return redirect(url_for('shop.cart'))


@shop.route('/cart/update', methods=['POST'])
@login_required
def update_cart():
    item_id = request.form.get('item_id', type=int)
    quantity = request.form.get('quantity', type=int)

    cart_item = CartItem.query.get_or_404(item_id)

    if cart_item.cart.user_id != current_user.id:
        return jsonify({'success': False, 'message': '无权操作'})

    if quantity <= 0:
        db.session.delete(cart_item)
    else:
        if quantity > cart_item.product.stock:
            return jsonify({'success': False, 'message': '库存不足'})
        cart_item.quantity = quantity

    db.session.commit()

    cart = Cart.query.filter_by(user_id=current_user.id).first()
    total_price = cart.get_total_price() if cart else 0

    return jsonify({
        'success': True,
        'item_total': cart_item.get_subtotal() if quantity > 0 else 0,
        'cart_total': total_price
    })


@shop.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart or cart.items.count() == 0:
        flash('购物车为空', 'warning')
        return redirect(url_for('shop.cart'))

    # 检查库存
    for item in cart.items:
        if item.quantity > item.product.stock:
            flash(f'商品"{item.product.name}"库存不足', 'danger')
            return redirect(url_for('shop.cart'))

    form = CheckoutForm()
    if form.validate_on_submit():
        # 创建订单
        order = Order(
            user_id=current_user.id,
            shipping_address=form.shipping_address.data,
            phone=form.phone.data,
            notes=form.notes.data
        )
        order.order_number = order.generate_order_number()

        total_amount = 0
        # 创建订单项并更新库存
        for cart_item in cart.items:
            order_item = OrderItem(
                order=order,
                product_id=cart_item.product_id,
                product_name=cart_item.product.name,
                product_price=cart_item.product.price,
                quantity=cart_item.quantity
            )
            total_amount += order_item.get_subtotal()

            # 更新库存
            cart_item.product.stock -= cart_item.quantity
            db.session.add(order_item)

        order.total_amount = total_amount

        # 清空购物车
        for cart_item in cart.items:
            db.session.delete(cart_item)

        # 记录日志
        log = UserLog(
            user_id=current_user.id,
            action='purchase',
            details=f'下单: {order.order_number}，总金额: ¥{total_amount}',
            ip_address=request.remote_addr
        )
        db.session.add(log)

        db.session.add(order)
        db.session.commit()

        flash('订单创建成功！', 'success')
        return redirect(url_for('shop.order_detail', order_id=order.id))

    return render_template('shop/checkout.html', form=form, cart=cart)


@shop.route('/orders')
@login_required
def orders():
    page = request.args.get('page', 1, type=int)
    orders = Order.query.filter_by(user_id=current_user.id) \
        .order_by(Order.created_at.desc()) \
        .paginate(page=page, per_page=10, error_out=False)

    return render_template('shop/orders.html', orders=orders)


@shop.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)

    if order.user_id != current_user.id:
        flash('无权查看此订单', 'danger')
        return redirect(url_for('shop.orders'))

    return render_template('shop/order_detail.html', order=order)


@shop.route('/review/<int:product_id>', methods=['POST'])
@login_required
def add_review(product_id):
    from app.models import Review

    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            user_id=current_user.id,
            product_id=product_id,
            rating=form.rating.data,
            comment=form.comment.data
        )

        db.session.add(review)
        db.session.commit()

        flash('评价提交成功', 'success')

    return redirect(url_for('main.product_detail', id=product_id))