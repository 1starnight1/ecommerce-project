"""
订单模块路由
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .. import db
from ..models import Order, OrderItem, CartItem, Product
from ..utils import generate_order_number, log_user_action, calculate_cart_total

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

@orders_bp.route('/')
@login_required
def order_list():
    """订单列表"""
    orders = Order.query.filter_by(user_id=current_user.id)\
                       .order_by(Order.created_at.desc())\
                       .all()
    
    return render_template('orders/list.html', orders=orders)

@orders_bp.route('/<int:order_id>')
@login_required
def order_detail(order_id):
    """订单详情"""
    order = Order.query.get_or_404(order_id)
    
    # 验证权限
    if order.user_id != current_user.id:
        flash('无权访问此订单', 'danger')
        return redirect(url_for('orders.order_list'))
    
    order_items = OrderItem.query.filter_by(order_id=order_id).all()
    
    return render_template('orders/detail.html',
                         order=order,
                         order_items=order_items)

@orders_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """结账"""
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    if not cart_items:
        flash('购物车为空，无法结账', 'warning')
        return redirect(url_for('cart.view_cart'))
    
    # 检查库存
    for item in cart_items:
        if item.product.stock < item.quantity:
            flash(f'商品"{item.product.name}"库存不足', 'danger')
            return redirect(url_for('cart.view_cart'))
    
    total = calculate_cart_total(cart_items)
    
    if request.method == 'POST':
        shipping_address = request.form.get('shipping_address', '').strip()
        contact_phone = request.form.get('contact_phone', '').strip()
        
        if not shipping_address:
            flash('请输入收货地址', 'danger')
            return render_template('orders/checkout.html',
                                 cart_items=cart_items,
                                 total=total)
        
        # 创建订单
        order = Order(
            user_id=current_user.id,
            order_number=generate_order_number(),
            total_amount=total,
            shipping_address=shipping_address,
            contact_phone=contact_phone
        )
        db.session.add(order)
        db.session.flush()  # 获取order.id
        
        # 创建订单项并更新库存
        for item in cart_items:
            # 创建订单项
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product.price
            )
            db.session.add(order_item)
            
            # 更新商品库存
            item.product.stock -= item.quantity
        
        # 清空购物车
        CartItem.query.filter_by(user_id=current_user.id).delete()
        
        db.session.commit()
        
        # 记录日志
        log_user_action(current_user.id, 'purchase', 
                       details=f"order_id: {order.id}, total: {total}")
        
        flash(f'订单创建成功！订单号：{order.order_number}', 'success')
        return redirect(url_for('orders.order_detail', order_id=order.id))
    
    return render_template('orders/checkout.html',
                         cart_items=cart_items,
                         total=total)

@orders_bp.route('/<int:order_id>/cancel', methods=['POST'])
@login_required
def cancel_order(order_id):
    """取消订单"""
    order = Order.query.get_or_404(order_id)
    
    # 验证权限
    if order.user_id != current_user.id:
        flash('无权操作', 'danger')
        return redirect(url_for('orders.order_list'))
    
    # 检查订单状态
    if order.status not in ['pending', 'paid']:
        flash('当前状态无法取消订单', 'danger')
        return redirect(url_for('orders.order_detail', order_id=order_id))
    
    # 恢复库存
    order_items = OrderItem.query.filter_by(order_id=order_id).all()
    for item in order_items:
        product = Product.query.get(item.product_id)
        if product:
            product.stock += item.quantity
    
    # 更新订单状态
    order.status = 'cancelled'
    db.session.commit()
    
    flash('订单已取消', 'success')
    return redirect(url_for('orders.order_detail', order_id=order_id))
