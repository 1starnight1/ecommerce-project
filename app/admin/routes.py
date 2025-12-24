from flask import redirect
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
