from flask import redirect
from flask_login import login_required, current_user
from . import bp


# 修改 app/main/routes.py 中的 index 函数
@bp.route('/')
def index():
    """首页 - 显示登录状态"""
    from flask_login import current_user

    if current_user.is_authenticated:
        # 用户已登录
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>电商管理系统 - 欢迎回来</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{ padding-top: 20px; }}
                .welcome-box {{ 
                    background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
                    color: white;
                    padding: 40px;
                    border-radius: 10px;
                    margin-bottom: 30px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <!-- 导航栏 -->
                <nav class="navbar navbar-light bg-white shadow-sm mb-4">
                    <div class="container-fluid">
                        <a class="navbar-brand text-primary fw-bold" href="/">
                            <i class="bi bi-shop"></i> 电商管理系统
                        </a>
                        <div class="navbar-nav">
                            <span class="nav-link">欢迎，{current_user.username}！</span>
                            <a class="nav-link text-danger" href="/auth/logout">退出</a>
                        </div>
                    </div>
                </nav>

                <!-- 欢迎信息 -->
                <div class="welcome-box text-center">
                    <h1 class="display-4">🎉 欢迎回来，{current_user.username}！</h1>
                    <p class="lead">您已成功登录电商管理系统</p>
                </div>

                <!-- 功能卡片 -->
                <div class="row mt-4">
                    <div class="col-md-4 mb-3">
                        <div class="card h-100 text-center">
                            <div class="card-body">
                                <h5 class="card-title">用户仪表盘</h5>
                                <p class="card-text">查看您的账户信息和统计数据</p>
                                <a href="/dashboard" class="btn btn-primary">进入仪表盘</a>
                            </div>
                        </div>
                    </div>

                    {f'''
                    <div class="col-md-4 mb-3">
                        <div class="card h-100 text-center">
                            <div class="card-body">
                                <h5 class="card-title text-danger">管理后台</h5>
                                <p class="card-text">管理员专属功能</p>
                                <a href="/admin" class="btn btn-danger">进入管理后台</a>
                            </div>
                        </div>
                    </div>
                    ''' if current_user.is_admin else ''}

                    <div class="col-md-4 mb-3">
                        <div class="card h-100 text-center">
                            <div class="card-body">
                                <h5 class="card-title">个人资料</h5>
                                <p class="card-text">查看和修改您的个人信息</p>
                                <a href="/profile" class="btn btn-secondary">个人资料</a>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 用户信息 -->
                <div class="card mt-4">
                    <div class="card-body">
                        <h5>账户信息</h5>
                        <table class="table">
                            <tr>
                                <td width="150"><strong>用户名：</strong></td>
                                <td>{current_user.username}</td>
                            </tr>
                            <tr>
                                <td><strong>邮箱：</strong></td>
                                <td>{current_user.email}</td>
                            </tr>
                            <tr>
                                <td><strong>账户类型：</strong></td>
                                <td><span class="badge bg-{'danger' if current_user.is_admin else 'success'}">
                                    {'管理员' if current_user.is_admin else '普通用户'}
                                </span></td>
                            </tr>
                            <tr>
                                <td><strong>注册时间：</strong></td>
                                <td>{current_user.created_at.strftime('%Y-%m-%d %H:%M:%S') if current_user.created_at else '未知'}</td>
                            </tr>
                        </table>
                    </div>
                </div>
            </div>

            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        </body>
        </html>
        """
    else:
        # 用户未登录 - 显示原始首页
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>电商管理系统</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
            <style>
                body { background-color: #f8f9fa; }
                .hero { 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 80px 0;
                    margin-bottom: 40px;
                }
                .feature-card { 
                    transition: transform 0.3s;
                    border: none;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
                }
                .feature-card:hover {
                    transform: translateY(-5px);
                }
            </style>
        </head>
        <body>
            <!-- 导航栏 -->
            <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
                <div class="container">
                    <a class="navbar-brand text-primary fw-bold" href="/">
                        <i class="bi bi-shop me-2"></i>电商管理系统
                    </a>
                    <div class="navbar-nav">
                        <a class="nav-link" href="/auth/login">登录</a>
                        <a class="btn btn-primary ms-2" href="/auth/register">注册</a>
                    </div>
                </div>
            </nav>

            <!-- 英雄区域 -->
            <div class="hero text-center">
                <div class="container">
                    <h1 class="display-4 fw-bold mb-4">专业的电商后台管理平台</h1>
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
                        <div class="card feature-card h-100 text-center p-4">
                            <div class="text-primary" style="font-size: 3rem;">
                                <i class="bi bi-people"></i>
                            </div>
                            <h4 class="mt-3">用户管理</h4>
                            <p>完整的用户权限管理系统</p>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card feature-card h-100 text-center p-4">
                            <div class="text-success" style="font-size: 3rem;">
                                <i class="bi bi-cart-check"></i>
                            </div>
                            <h4 class="mt-3">订单处理</h4>
                            <p>全流程订单管理系统</p>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card feature-card h-100 text-center p-4">
                            <div class="text-info" style="font-size: 3rem;">
                                <i class="bi bi-bar-chart"></i>
                            </div>
                            <h4 class="mt-3">数据分析</h4>
                            <p>详细的销售数据分析</p>
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
