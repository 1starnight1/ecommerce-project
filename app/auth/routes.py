from flask import redirect, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, UserLog
from datetime import datetime
from . import bp

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """登录页面"""
    if current_user.is_authenticated:
        return redirect('/')

    # 获取可能的错误消息
    error_msg = ""
    success_msg = ""

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            if user.is_active:
                login_user(user, remember=True)
                user.last_login = datetime.utcnow()
                db.session.commit()

                # 记录日志
                log = UserLog(
                    user_id=user.id,
                    action='LOGIN',
                    details='用户登录系统',
                    ip_address=request.remote_addr,
                    user_agent=request.user_agent.string
                )
                db.session.add(log)
                db.session.commit()

                # 重定向到仪表盘
                return redirect('/dashboard')
            else:
                error_msg = "账户已被禁用，请联系管理员"
        else:
            error_msg = "用户名或密码错误"

    # 从URL参数获取用户名（用于测试账户快速登录）
    username = request.args.get('username', '')

    return f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>用户登录 - 电商管理系统</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
        <style>
            body {{ background-color: #f8f9fa; }}
            .login-card {{ max-width: 400px; margin: 60px auto; }}
            .form-control {{ padding: 10px 15px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="login-card card shadow-lg">
                <div class="card-header bg-primary text-white text-center py-4">
                    <h3 class="mb-0"><i class="bi bi-box-arrow-in-right me-2"></i>用户登录</h3>
                </div>
                <div class="card-body p-4">
                    {f'<div class="alert alert-danger">{error_msg}</div>' if error_msg else ''}
                    {f'<div class="alert alert-success">{success_msg}</div>' if success_msg else ''}

                    <form method="POST" action="/auth/login">
                        <div class="mb-3">
                            <label class="form-label">用户名</label>
                            <input type="text" class="form-control" name="username" value="{username}" 
                                   placeholder="请输入用户名" required autofocus>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">密码</label>
                            <input type="password" class="form-control" name="password" 
                                   placeholder="请输入密码" required>
                        </div>
                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary btn-lg">
                                <i class="bi bi-box-arrow-in-right me-2"></i>登录系统
                            </button>
                        </div>
                    </form>

                    <hr class="my-4">

                    <div class="text-center">
                        <p class="text-muted mb-2">还没有账户？</p>
                        <a href="/auth/register" class="btn btn-outline-primary">
                            <i class="bi bi-person-plus me-2"></i>立即注册
                        </a>
                    </div>

                    <div class="mt-4">
                        <h6 class="text-center text-muted">测试账户</h6>
                        <div class="d-flex justify-content-center gap-2">
                            <a href="/auth/login?username=admin" class="btn btn-sm btn-outline-primary">管理员</a>
                            <a href="/auth/login?username=testuser" class="btn btn-sm btn-outline-secondary">普通用户</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """注册页面"""
    if current_user.is_authenticated:
        return redirect('/')

    error_msg = ""
    success_msg = ""

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # 验证
        if password != confirm_password:
            error_msg = "两次输入的密码不一致"
        elif User.query.filter_by(username=username).first():
            error_msg = "用户名已存在"
        elif User.query.filter_by(email=email).first():
            error_msg = "邮箱已存在"
        else:
            # 创建用户
            user = User(username=username, email=email, is_active=True)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            # 记录日志
            log = UserLog(
                user_id=user.id,
                action='REGISTER',
                details='新用户注册',
                ip_address=request.remote_addr,
                user_agent=request.user_agent.string
            )
            db.session.add(log)
            db.session.commit()

            success_msg = "注册成功！3秒后跳转到登录页面"
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>注册成功</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            </head>
            <body>
                <div class="container mt-5 text-center">
                    <div class="alert alert-success">
                        <h4>注册成功！</h4>
                        <p>账户 {username} 已创建成功</p>
                    </div>
                    <p>正在跳转到登录页面...</p>
                    <a href="/auth/login" class="btn btn-primary">立即登录</a>
                    <script>
                        setTimeout(function() {{
                            window.location.href = "/auth/login";
                        }}, 3000);
                    </script>
                </div>
            </body>
            </html>
            """

    return f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>用户注册 - 电商管理系统</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
        <style>
            body {{ background-color: #f8f9fa; }}
            .register-card {{ max-width: 500px; margin: 40px auto; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="register-card card shadow-lg">
                <div class="card-header bg-success text-white text-center py-4">
                    <h3 class="mb-0"><i class="bi bi-person-plus me-2"></i>用户注册</h3>
                </div>
                <div class="card-body p-4">
                    {f'<div class="alert alert-danger">{error_msg}</div>' if error_msg else ''}

                    <form method="POST" action="/auth/register">
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">用户名</label>
                                <input type="text" class="form-control" name="username" 
                                       placeholder="请输入用户名" required>
                                <div class="form-text">3-20个字符</div>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">邮箱地址</label>
                                <input type="email" class="form-control" name="email" 
                                       placeholder="example@domain.com" required>
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">密码</label>
                                <input type="password" class="form-control" name="password" 
                                       placeholder="请输入密码" required>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">确认密码</label>
                                <input type="password" class="form-control" name="confirm_password" 
                                       placeholder="请再次输入密码" required>
                            </div>
                        </div>

                        <div class="mb-4">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="terms" required>
                                <label class="form-check-label" for="terms">
                                    我已阅读并同意服务条款
                                </label>
                            </div>
                        </div>

                        <div class="d-grid">
                            <button type="submit" class="btn btn-success btn-lg">
                                <i class="bi bi-person-plus me-2"></i>注册账户
                            </button>
                        </div>
                    </form>

                    <hr class="my-4">

                    <div class="text-center">
                        <p class="text-muted mb-2">已有账户？</p>
                        <a href="/auth/login" class="btn btn-outline-primary">
                            <i class="bi bi-box-arrow-in-right me-2"></i>立即登录
                        </a>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """

@bp.route('/logout')
@login_required
def logout():
    """登出"""
    logout_user()
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>登出成功</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5 text-center">
            <h1 class="text-success">✅ 登出成功</h1>
            <p class="lead">您已成功退出系统</p>
            <a href="/" class="btn btn-primary mt-3">返回首页</a>
            <script>
                setTimeout(function() {
                    window.location.href = "/";
                }, 2000);
            </script>
        </div>
    </body>
    </html>
    """
