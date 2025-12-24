# complete_fix.py
import os
import shutil


def complete_fix():
    """完全修复所有路由文件"""

    print("开始完全修复所有路由文件...")

    # 1. 修复 main/routes.py
    main_content = '''from flask import redirect
from flask_login import login_required, current_user
from . import bp

@bp.route('/')
def index():
    """首页"""
    return """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>电商管理系统</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
        <style>
            body { font-family: "Microsoft YaHei", sans-serif; background-color: #f8f9fa; }
            .navbar { box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .hero-section { background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%); color: white; padding: 80px 0; }
            .feature-icon { font-size: 3rem; margin-bottom: 20px; }
            .card { border: none; box-shadow: 0 5px 15px rgba(0,0,0,0.08); transition: transform 0.3s; }
            .card:hover { transform: translateY(-5px); }
        </style>
    </head>
    <body>
        <!-- 导航栏 -->
        <nav class="navbar navbar-expand-lg navbar-light bg-white">
            <div class="container">
                <a class="navbar-brand text-primary fw-bold" href="/">
                    <i class="bi bi-shop me-2"></i>电商管理系统
                </a>
                <div class="navbar-nav ms-auto">
                    <a class="nav-link" href="/auth/login">登录</a>
                    <a class="btn btn-primary ms-2" href="/auth/register">注册</a>
                </div>
            </div>
        </nav>

        <!-- 英雄区域 -->
        <div class="hero-section text-center">
            <div class="container">
                <h1 class="display-4 fw-bold mb-4">专业电商后台管理平台</h1>
                <p class="lead mb-4">一站式解决用户管理、订单处理、数据分析需求</p>
                <div class="mt-4">
                    <a href="/auth/login" class="btn btn-light btn-lg me-3 px-4">
                        <i class="bi bi-box-arrow-in-right me-2"></i>立即登录
                    </a>
                    <a href="/auth/register" class="btn btn-outline-light btn-lg px-4">
                        <i class="bi bi-person-plus me-2"></i>免费注册
                    </a>
                </div>
            </div>
        </div>

        <!-- 功能特性 -->
        <div class="container py-5">
            <h2 class="text-center mb-5">核心功能</h2>
            <div class="row g-4">
                <div class="col-md-4">
                    <div class="card h-100 text-center p-4">
                        <div class="text-primary feature-icon">
                            <i class="bi bi-people"></i>
                        </div>
                        <h4>用户管理</h4>
                        <p>完整的用户权限管理系统，支持角色分配、权限控制、用户统计</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card h-100 text-center p-4">
                        <div class="text-success feature-icon">
                            <i class="bi bi-cart-check"></i>
                        </div>
                        <h4>订单处理</h4>
                        <p>全流程订单管理系统，支持多种支付方式、物流跟踪、订单统计</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card h-100 text-center p-4">
                        <div class="text-info feature-icon">
                            <i class="bi bi-bar-chart"></i>
                        </div>
                        <h4>数据分析</h4>
                        <p>详细的销售数据分析和报表，助力业务决策和运营优化</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- 测试账户 -->
        <div class="container pb-5">
            <div class="card">
                <div class="card-body">
                    <h4 class="card-title text-center mb-4">
                        <i class="bi bi-key me-2"></i>测试账户
                    </h4>
                    <div class="row">
                        <div class="col-md-6">
                            <div class="card border-primary mb-3">
                                <div class="card-header bg-primary text-white">
                                    <strong>管理员账户</strong>
                                </div>
                                <div class="card-body">
                                    <p><i class="bi bi-person me-2"></i>用户名: <code>admin</code></p>
                                    <p><i class="bi bi-lock me-2"></i>密码: <code>admin123</code></p>
                                    <a href="/auth/login?username=admin" class="btn btn-outline-primary w-100">
                                        使用此账户登录
                                    </a>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="card border-secondary mb-3">
                                <div class="card-header bg-secondary text-white">
                                    <strong>普通用户</strong>
                                </div>
                                <div class="card-body">
                                    <p><i class="bi bi-person me-2"></i>用户名: <code>testuser</code></p>
                                    <p><i class="bi bi-lock me-2"></i>密码: <code>test123</code></p>
                                    <a href="/auth/login?username=testuser" class="btn btn-outline-secondary w-100">
                                        使用此账户登录
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 页脚 -->
        <footer class="bg-dark text-white py-4">
            <div class="container text-center">
                <p class="mb-0">© 2024 电商管理系统 | 专业电商后台解决方案</p>
            </div>
        </footer>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """

@bp.route('/dashboard')
@login_required
def dashboard():
    """用户仪表盘"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>用户仪表盘</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <nav class="navbar navbar-light bg-white shadow-sm">
            <div class="container">
                <a class="navbar-brand" href="/">电商管理系统</a>
                <div class="navbar-nav">
                    <span class="nav-link">欢迎，{current_user.username}</span>
                    <a class="nav-link text-danger" href="/auth/logout">退出</a>
                </div>
            </div>
        </nav>

        <div class="container mt-5">
            <h1>用户仪表盘</h1>
            <div class="card mt-4">
                <div class="card-body">
                    <h5>用户信息</h5>
                    <p>用户名: {current_user.username}</p>
                    <p>邮箱: {current_user.email}</p>
                    <p>账户类型: {"管理员" if current_user.is_admin else "普通用户"}</p>
                </div>
            </div>
            <a href="/" class="btn btn-primary mt-3">返回首页</a>
        </div>
    </body>
    </html>
    """

@bp.route('/profile')
@login_required
def profile():
    """个人资料"""
    return """
    <!DOCTYPE html>
    <html>
    <head><title>个人资料</title></head>
    <body>
        <h1>个人资料页面</h1>
        <p>正在开发中...</p>
        <a href="/">返回首页</a>
    </body>
    </html>
    """
'''

    with open("app/main/routes.py", "w", encoding="utf-8") as f:
        f.write(main_content)
    print("✅ 修复: app/main/routes.py")

    # 2. 修复 auth/routes.py
    auth_content = '''from flask import redirect, request, flash
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
'''

    with open("app/auth/routes.py", "w", encoding="utf-8") as f:
        f.write(auth_content)
    print("✅ 修复: app/auth/routes.py")

    # 3. 修复 admin/routes.py
    admin_content = '''from flask import redirect
from flask_login import login_required, current_user
from . import bp

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            return """
            <!DOCTYPE html>
            <html>
            <head><title>权限不足</title></head>
            <body>
                <h1>❌ 权限不足</h1>
                <p>您没有访问此页面的权限</p>
                <a href="/">返回首页</a>
            </body>
            </html>
            """, 403
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@login_required
@admin_required
def dashboard():
    """管理后台"""
    return f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>管理后台 - 电商管理系统</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
        <style>
            body {{ background-color: #f8f9fa; }}
            .admin-header {{ background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); color: white; }}
            .stat-card {{ border-left: 4px solid; }}
        </style>
    </head>
    <body>
        <!-- 导航栏 -->
        <nav class="navbar navbar-expand-lg navbar-dark admin-header shadow">
            <div class="container">
                <a class="navbar-brand fw-bold" href="/admin">
                    <i class="bi bi-shield-check me-2"></i>管理后台
                </a>
                <div class="navbar-nav ms-auto">
                    <span class="nav-link">管理员: {current_user.username}</span>
                    <a class="nav-link" href="/">返回前台</a>
                    <a class="nav-link text-warning" href="/auth/logout">退出</a>
                </div>
            </div>
        </nav>

        <div class="container py-5">
            <h2 class="mb-4"><i class="bi bi-speedometer2 me-2"></i>管理仪表盘</h2>

            <!-- 统计卡片 -->
            <div class="row g-4 mb-5">
                <div class="col-md-3">
                    <div class="card stat-card border-left-primary h-100">
                        <div class="card-body">
                            <h6 class="text-muted">总用户数</h6>
                            <h3 class="text-primary">0</h3>
                            <a href="/admin/users" class="btn btn-sm btn-outline-primary">管理用户</a>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card stat-card border-left-success h-100">
                        <div class="card-body">
                            <h6 class="text-muted">总订单数</h6>
                            <h3 class="text-success">0</h3>
                            <a href="/admin/orders" class="btn btn-sm btn-outline-success">管理订单</a>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card stat-card border-left-info h-100">
                        <div class="card-body">
                            <h6 class="text-muted">总销售额</h6>
                            <h3 class="text-info">¥0.00</h3>
                            <a href="/admin/statistics" class="btn btn-sm btn-outline-info">查看统计</a>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card stat-card border-left-warning h-100">
                        <div class="card-body">
                            <h6 class="text-muted">今日订单</h6>
                            <h3 class="text-warning">0</h3>
                            <small class="text-muted">今日收入: ¥0.00</small>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 快速操作 -->
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0"><i class="bi bi-lightning me-2"></i>快速操作</h5>
                </div>
                <div class="card-body">
                    <div class="row g-3">
                        <div class="col-md-3">
                            <a href="/admin/users" class="btn btn-outline-primary w-100">
                                <i class="bi bi-people me-2"></i>用户管理
                            </a>
                        </div>
                        <div class="col-md-3">
                            <a href="/admin/orders" class="btn btn-outline-success w-100">
                                <i class="bi bi-cart me-2"></i>订单管理
                            </a>
                        </div>
                        <div class="col-md-3">
                            <a href="/admin/products" class="btn btn-outline-info w-100">
                                <i class="bi bi-grid me-2"></i>商品管理
                            </a>
                        </div>
                        <div class="col-md-3">
                            <a href="/admin/logs" class="btn btn-outline-secondary w-100">
                                <i class="bi bi-clock-history me-2"></i>操作日志
                            </a>
                        </div>
                    </div>
                </div>
            </div>

            <div class="alert alert-info mt-4">
                <i class="bi bi-info-circle me-2"></i>
                <strong>提示：</strong> 使用 <code>flask init_db</code> 命令初始化测试数据
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """

@bp.route('/users')
@login_required
@admin_required
def manage_users():
    """用户管理"""
    return """
    <!DOCTYPE html>
    <html>
    <head><title>用户管理</title></head>
    <body>
        <div class="container mt-5">
            <h1>用户管理</h1>
            <p>用户管理功能正在开发中...</p>
            <a href="/admin" class="btn btn-primary">返回管理后台</a>
        </div>
    </body>
    </html>
    """

@bp.route('/orders')
@login_required
@admin_required
def manage_orders():
    """订单管理"""
    return """
    <!DOCTYPE html>
    <html>
    <head><title>订单管理</title></head>
    <body>
        <div class="container mt-5">
            <h1>订单管理</h1>
            <p>订单管理功能正在开发中...</p>
            <a href="/admin" class="btn btn-success">返回管理后台</a>
        </div>
    </body>
    </html>
    """
'''

    with open("app/admin/routes.py", "w", encoding="utf-8") as f:
        f.write(admin_content)
    print("✅ 修复: app/admin/routes.py")

    print("\n" + "=" * 50)
    print("✅ 完全修复完成！")
    print("=" * 50)
    print("\n现在可以运行应用了：")
    print("1. 运行: python run.py")
    print("2. 访问: http://127.0.0.1:5000/")
    print("3. 测试账户:")
    print("   - 管理员: admin / admin123")
    print("   - 普通用户: testuser / test123")


if __name__ == "__main__":
    complete_fix()