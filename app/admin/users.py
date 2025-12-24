# app/admin/users.py
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import or_, func
from datetime import datetime, timedelta
from app import db
from app.models import User, UserLog, Order, Product
from . import bp


@bp.route('/users')
@login_required
def manage_users():
    """用户管理页面"""
    if not current_user.is_admin:
        flash('权限不足', 'error')
        return redirect(url_for('main.index'))

    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')

    query = User.query

    if search:
        query = query.filter(
            or_(
                User.username.ilike(f'%{search}%'),
                User.email.ilike(f'%{search}%'),
                User.phone.ilike(f'%{search}%')
            )
        )

    users = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    # 统计信息
    total_users = User.query.count()
    admin_count = User.query.filter_by(is_admin=True).count()
    active_count = User.query.filter_by(is_active=True).count()

    return render_template(
        'admin/manage_users.html',
        users=users,
        search=search,
        total_users=total_users,
        admin_count=admin_count,
        active_count=active_count
    )


@bp.route('/users/<int:user_id>')
@login_required
def user_detail(user_id):
    """用户详情"""
    if not current_user.is_admin:
        flash('权限不足', 'error')
        return redirect(url_for('main.index'))

    user = User.query.get_or_404(user_id)

    # 用户统计
    order_count = Order.query.filter_by(user_id=user_id).count()
    total_spent = db.session.query(func.sum(Order.total_amount)).filter_by(user_id=user_id).scalar() or 0

    # 最近订单
    recent_orders = Order.query.filter_by(user_id=user_id).order_by(
        Order.created_at.desc()
    ).limit(5).all()

    # 最近登录日志
    recent_logs = UserLog.query.filter_by(user_id=user_id).order_by(
        UserLog.created_at.desc()
    ).limit(10).all()

    return render_template(
        'admin/user_detail.html',
        user=user,
        order_count=order_count,
        total_spent=total_spent,
        recent_orders=recent_orders,
        recent_logs=recent_logs
    )

# 添加之前提到的所有用户管理路由函数...
# (toggle_user_active, make_user_admin, remove_user_admin, delete_user, reset_user_password, export_users, logs等)