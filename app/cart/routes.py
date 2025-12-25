from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Product, Cart, CartItem
from datetime import datetime  # 添加这行

# 使用与__init__.py中一致的蓝图名称
from app.cart import cart


@cart.route('/')
@login_required
def view_cart():
    """查看购物车"""
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()

    # 修改为：直接使用模板名，因为模板在 app/cart/templates/view.html
    return render_template('view.html', cart=cart, now=datetime.now())


@cart.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    """添加商品到购物车"""
    product = Product.query.get_or_404(product_id)

    # 检查库存
    quantity = request.form.get('quantity', 1, type=int)
    if product.stock < quantity:
        flash('库存不足', 'error')
        return redirect(request.referrer or url_for('main.index'))

    # 获取或创建购物车
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()

    # 检查是否已在购物车中
    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity,
            price=product.price
        )
        db.session.add(cart_item)

    db.session.commit()
    flash(f'已添加 {product.name} 到购物车', 'success')

    # 如果是AJAX请求，返回JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'success': True,
            'message': f'已添加 {product.name} 到购物车',
            'cart_items_count': cart.total_quantity
        })

    return redirect(request.referrer or url_for('main.index'))


@cart.route('/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart_item(item_id):
    """更新购物车项数量"""
    cart_item = CartItem.query.get_or_404(item_id)

    # 验证用户权限
    if cart_item.cart.user_id != current_user.id:
        flash('无权操作', 'error')
        return redirect(url_for('cart.view_cart'))

    quantity = request.form.get('quantity', 1, type=int)

    # 检查库存
    if cart_item.product.stock < quantity:
        flash('库存不足', 'error')
        return redirect(url_for('cart.view_cart'))

    cart_item.quantity = quantity
    db.session.commit()
    flash('购物车已更新', 'success')
    return redirect(url_for('cart.view_cart'))


@cart.route('/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    """从购物车移除商品"""
    cart_item = CartItem.query.get_or_404(item_id)

    # 验证用户权限
    if cart_item.cart.user_id != current_user.id:
        flash('无权操作', 'error')
        return redirect(url_for('cart.view_cart'))

    db.session.delete(cart_item)
    db.session.commit()
    flash('已从购物车移除商品', 'success')
    return redirect(url_for('cart.view_cart'))


@cart.route('/clear', methods=['POST'])
@login_required
def clear_cart():
    """清空购物车"""
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if cart:
        cart.items.delete()
        db.session.commit()
        flash('购物车已清空', 'success')
    return redirect(url_for('cart.view_cart'))


# 添加调试路由
@cart.route('/test')
def test():
    """测试模板是否能加载"""
    try:
        cart = Cart.query.filter_by(user_id=current_user.id).first() if current_user.is_authenticated else None
        return render_template('view.html', cart=cart, now=datetime.now(), test="测试成功")
    except Exception as e:
        return f"模板加载错误: {str(e)}", 500