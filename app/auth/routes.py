from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import User, UserLog
from app.auth import auth
from datetime import datetime

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """登录页面"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('账户已被禁用，请联系管理员', 'danger')
                return redirect(url_for('auth.login'))
            
            login_user(user)
            
            # 更新最后登录时间
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            flash(f'登录成功！欢迎回来，{user.username}！', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('用户名或密码错误', 'danger')
    
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    """退出登录"""
    username = current_user.username
    logout_user()
    flash(f'用户 {username} 已退出登录', 'info')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """注册页面"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    return render_template('register.html')

@auth.route('/profile')
@login_required
def profile():
    """个人资料页面"""
    return render_template('profile.html')
