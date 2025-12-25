from flask import render_template
from app import db

def register_error_handlers(app):
    """注册错误处理器"""
    
    @app.errorhandler(404)
    def not_found_error(error):
        if app.debug:
            return f"404 Not Found: {error}", 404
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        if app.debug:
            return f"500 Internal Server Error: {error}", 500
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        if app.debug:
            return f"403 Forbidden: {error}", 403
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(400)
    def bad_request_error(error):
        if app.debug:
            return f"400 Bad Request: {error}", 400
        return render_template('errors/400.html'), 400
