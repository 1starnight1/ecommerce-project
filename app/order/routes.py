from flask import Blueprint, render_template, redirect, url_for, flash, request, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Cart, CartItem, Order, OrderItem, Product
import random
import time  # 添加这行
from datetime import datetime

order_bp = Blueprint('order', __name__, url_prefix='/order')


@order_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """结算页面"""
    cart = Cart.query.filter_by(user_id=current_user.id).first()

    if not cart or cart.total_quantity == 0:
        flash('购物车为空', 'error')
        return redirect(url_for('cart.view_cart'))

    if request.method == 'POST':
        # 验证库存
        for item in cart.items:
            if item.product.stock < item.quantity:
                flash(f'{item.product.name} 库存不足，仅剩 {item.product.stock} 件', 'error')
                return redirect(url_for('cart.view_cart'))

        # 生成订单号
        def generate_order_number():
            return f"ORD{int(time.time())}{random.randint(1000, 9999)}"

        # 创建订单
        order = Order(
            order_number=generate_order_number(),
            user_id=current_user.id,
            total_amount=cart.total_price,
            shipping_address=request.form.get('shipping_address', ''),
            payment_method=request.form.get('payment_method', 'credit_card'),
            notes=request.form.get('notes', '')
        )
        db.session.add(order)
        db.session.flush()  # 获取order.id但不提交

        # 创建订单项并减少库存
        for cart_item in cart.items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.price,
                subtotal=cart_item.subtotal
            )
            db.session.add(order_item)

            # 减少库存
            cart_item.product.stock -= cart_item.quantity

        # 清空购物车
        cart.items.delete()

        db.session.commit()
        flash(f'订单创建成功！订单号：{order.order_number}', 'success')
        return redirect(url_for('order.order_detail', order_id=order.id))

    # 修改为：直接使用模板名，因为模板在 app/order/templates/checkout.html
    return render_template('checkout.html', cart=cart, now=datetime.now())


@order_bp.route('/<int:order_id>')
@login_required
def order_detail(order_id):
    """订单详情"""
    order = Order.query.get_or_404(order_id)

    # 验证用户权限
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('无权查看此订单', 'error')
        return redirect(url_for('main.index'))

    # 注意：这里需要修改，因为 order/detail.html 可能不存在
    # 先尝试渲染简单的详情页面
    return render_template('checkout.html', cart=None, order=order, now=datetime.now())


@order_bp.route('/list')
@login_required
def order_list():
    """订单列表"""
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()

    # 创建简单的订单列表页面
    return f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"><title>我的订单</title></head>
    <body>
        <h1>我的订单</h1>
        <ul>
        {''.join(f'<li>订单号: {order.order_number} - 金额: ¥{order.total_amount} - 状态: {order.status}</li>' for order in orders)}
        </ul>
        <a href="/">返回首页</a>
    </body>
    </html>
    """
    # 或者如果 order/list.html 不存在，可以暂时用这个


@order_bp.route('/cancel/<int:order_id>', methods=['POST'])
@login_required
def cancel_order(order_id):
    """取消订单"""
    order = Order.query.get_or_404(order_id)

    # 验证用户权限
    if order.user_id != current_user.id:
        flash('无权操作', 'error')
        return redirect(url_for('order.order_list'))

    # 只有待处理订单可以取消
    if order.status != 'pending':
        flash('只有待处理订单可以取消', 'error')
        return redirect(url_for('order.order_detail', order_id=order_id))

    # 恢复库存
    for item in order.items:
        product = Product.query.get(item.product_id)
        if product:
            product.stock += item.quantity

    order.status = 'cancelled'
    db.session.commit()
    flash('订单已取消', 'success')
    return redirect(url_for('order.order_detail', order_id=order_id))


# 添加调试路由
@order_bp.route('/test')
def test():
    """测试模板是否能加载"""
    try:
        return render_template('checkout.html', cart=None, test="测试成功")
    except Exception as e:
        return f"模板加载错误: {str(e)}", 500