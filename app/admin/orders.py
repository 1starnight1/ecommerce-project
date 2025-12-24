# app/admin/orders.py
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import or_, func
from datetime import datetime, timedelta
from app import db
from app.models import Order, OrderItem, Product, User, UserLog
from . import bp


@bp.route('/orders')
@login_required
def manage_orders():
    """订单管理页面"""
    if not current_user.is_admin:
        flash('权限不足', 'error')
        return redirect(url_for('main.index'))

    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')

    query = Order.query

    # 搜索条件
    if search:
        query = query.filter(
            or_(
                Order.order_number.ilike(f'%{search}%'),
                User.username.ilike(f'%{search}%'),
                User.email.ilike(f'%{search}%')
            )
        )

    if status:
        query = query.filter_by(status=status)

    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
            query = query.filter(Order.created_at >= date_from_obj)
        except ValueError:
            pass

    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1)
            query = query.filter(Order.created_at <= date_to_obj)
        except ValueError:
            pass

    # 分页查询
    orders = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    # 统计信息
    total_orders = Order.query.count()
    total_revenue = db.session.query(func.sum(Order.total_amount)).scalar() or 0

    return render_template(
        'admin/manage_orders.html',
        orders=orders,
        search=search,
        status=status,
        date_from=date_from,
        date_to=date_to,
        total_orders=total_orders,
        total_revenue=total_revenue
    )


@bp.route('/orders/<int:order_id>')
@login_required
def order_detail(order_id):
    """订单详情"""
    if not current_user.is_admin:
        flash('权限不足', 'error')
        return redirect(url_for('main.index'))

    order = Order.query.get_or_404(order_id)
    return render_template('admin/order_detail.html', order=order)


@bp.route('/orders/<int:order_id>/update_status', methods=['POST'])
@login_required
def update_order_status(order_id):
    """更新订单状态"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': '权限不足'})

    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')

    if new_status not in ['pending', 'paid', 'shipped', 'completed', 'cancelled']:
        return jsonify({'success': False, 'message': '无效的状态'})

    # 更新状态和时间戳
    order.status = new_status
    if new_status == 'paid' and order.paid_at is None:
        order.paid_at = datetime.utcnow()
    elif new_status == 'shipped' and order.shipped_at is None:
        order.shipped_at = datetime.utcnow()
    elif new_status == 'completed' and order.completed_at is None:
        order.completed_at = datetime.utcnow()

    db.session.commit()

    # 记录日志
    log = UserLog(
        user_id=current_user.id,
        action='UPDATE_ORDER_STATUS',
        details=f'更新订单 {order.order_number} 状态为 {new_status}',
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': '订单状态已更新',
        'status_text': order.get_status_text(),
        'status_color': order.get_status_color()
    })


@bp.route('/orders/<int:order_id>/delete', methods=['POST'])
@login_required
def delete_order(order_id):
    """删除订单"""
    if not current_user.is_admin:
        flash('权限不足', 'error')
        return redirect(url_for('admin.manage_orders'))

    order = Order.query.get_or_404(order_id)

    # 记录日志
    log = UserLog(
        user_id=current_user.id,
        action='DELETE_ORDER',
        details=f'删除订单 {order.order_number}',
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string
    )

    db.session.add(log)
    db.session.delete(order)
    db.session.commit()

    flash(f'订单 {order.order_number} 已删除', 'success')
    return redirect(url_for('admin.manage_orders'))


@bp.route('/orders/export')
@login_required
def export_orders():
    """导出订单数据"""
    if not current_user.is_admin:
        flash('权限不足', 'error')
        return redirect(url_for('admin.manage_orders'))

    import csv
    from io import StringIO

    output = StringIO()
    writer = csv.writer(output)

    # 写入标题
    writer.writerow([
        '订单号', '用户名', '邮箱', '总金额', '状态', '支付方式',
        '收货地址', '下单时间', '支付时间', '发货时间', '完成时间'
    ])

    # 写入数据
    orders = Order.query.order_by(Order.created_at.desc()).all()
    for order in orders:
        writer.writerow([
            order.order_number,
            order.user.username,
            order.user.email,
            order.total_amount,
            order.get_status_text(),
            order.payment_method or '',
            order.shipping_address or '',
            order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            order.paid_at.strftime('%Y-%m-%d %H:%M:%S') if order.paid_at else '',
            order.shipped_at.strftime('%Y-%m-%d %H:%M:%S') if order.shipped_at else '',
            order.completed_at.strftime('%Y-%m-%d %H:%M:%S') if order.completed_at else ''
        ])

    output.seek(0)

    # 记录日志
    log = UserLog(
        user_id=current_user.id,
        action='EXPORT_ORDERS',
        details='导出订单数据',
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string
    )
    db.session.add(log)
    db.session.commit()

    from flask import Response
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=orders_export.csv'}
    )


@bp.route('/orders/statistics')
@login_required
def order_statistics():
    """订单统计"""
    if not current_user.is_admin:
        flash('权限不足', 'error')
        return redirect(url_for('main.index'))

    # 最近30天数据
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)

    # 每日订单统计
    daily_stats = db.session.query(
        func.date(Order.created_at).label('date'),
        func.count(Order.id).label('count'),
        func.sum(Order.total_amount).label('revenue')
    ).filter(
        Order.created_at >= thirty_days_ago
    ).group_by(
        func.date(Order.created_at)
    ).order_by(
        func.date(Order.created_at)
    ).all()

    # 状态统计
    status_stats = db.session.query(
        Order.status,
        func.count(Order.id).label('count')
    ).group_by(
        Order.status
    ).all()

    # 热门商品
    popular_products = db.session.query(
        Product.name,
        func.sum(OrderItem.quantity).label('total_sold'),
        func.sum(OrderItem.subtotal).label('total_revenue')
    ).join(
        OrderItem, OrderItem.product_id == Product.id
    ).group_by(
        Product.id, Product.name
    ).order_by(
        func.sum(OrderItem.quantity).desc()
    ).limit(10).all()

    # 最近一周数据
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_orders = Order.query.filter(
        Order.created_at >= week_ago
    ).order_by(
        Order.created_at.desc()
    ).limit(10).all()

    return render_template(
        'admin/order_statistics.html',
        daily_stats=daily_stats,
        status_stats=status_stats,
        popular_products=popular_products,
        recent_orders=recent_orders
    )