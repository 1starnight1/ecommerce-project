# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录以访问此页面'
login_manager.login_message_category = 'info'


def create_app(config_name='default'):
    """应用工厂函数"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # 注册蓝本
    register_blueprints(app)

    return app


def register_blueprints(app):
    """注册蓝图"""
    # 从各个模块导入蓝图
    from .main import bp as main_bp
    from .auth import bp as auth_bp
    from .admin import bp as admin_bp

    # 注册蓝图，确保使用正确的名称
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')