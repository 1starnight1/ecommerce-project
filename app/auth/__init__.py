# app/auth/__init__.py
from flask import Blueprint

# 认证蓝图
bp = Blueprint('auth', __name__)

from . import routes