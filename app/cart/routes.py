"""
购物车模块路由
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from .. import db
from ..models import CartItem, Product
from ..utils import log_user_action, calculate_cart_total

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

@cart_bp.route('/')
@login_required
def view_cart():
    """查看购物车"""
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = calculate_cart_total(cart_items)
    
    return render_template('cart/view.html',
                         cart_items=cart_items,
                         total=total)

@cart_bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    """添加商品到购物车"""
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    
    if quantity <= 0:
        flash('数量必须大于0', 'danger')
        return redirect(url_for('products.product_detail', product_id=product_id))
    
    # 检查库存
    if product.stock < quantity:
        flash('库存不足', 'danger')
        return redirect(url_for('products.product_detail', product_id=product_id))
    
    # 检查是否已在购物车
    cart_item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()
    
    if cart_item:
        # 检查总数量是否超过库存
        if cart_item.quantity + quantity > product.stock:
            flash('库存不足', 'danger')
            return redirect(url_for('products.product_detail', product_id=product_id))
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            user_id=current_user.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
    
    db.session.commit()
    
    log_user_action(current_user.id, 'add_to_cart', product_id, 
                   f"quantity: {quantity}")
    
    flash('商品已添加到购物车', 'success')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart_item(item_id):
    """更新购物车商品数量"""
    cart_item = CartItem.query.get_or_404(item_id)
    
    # 验证权限
    if cart_item.user_id != current_user.id:
        flash('无权操作', 'danger')
        return redirect(url_for('cart.view_cart'))
    
    quantity = int(request.form.get('quantity', 1))
    
    if quantity <= 0:
        # 删除商品
        db.session.delete(cart_item)
    else:
        # 检查库存
        if cart_item.product.stock < quantity:
            flash('库存不足', 'danger')
            return redirect(url_for('cart.view_cart'))
        
        # 更新数量
        cart_item.quantity = quantity
    
    db.session.commit()
    flash('购物车已更新', 'success')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    """从购物车移除商品"""
    cart_item = CartItem.query.get_or_404(item_id)
    
    # 验证权限
    if cart_item.user_id != current_user.id:
        flash('无权操作', 'danger')
        return redirect(url_for('cart.view_cart'))
    
    db.session.delete(cart_item)
    db.session.commit()
    
    flash('商品已从购物车移除', 'success')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/clear', methods=['POST'])
@login_required
def clear_cart():
    """清空购物车"""
    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    
    flash('购物车已清空', 'success')
    return redirect(url_for('cart.view_cart'))
