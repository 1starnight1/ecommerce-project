# app/admin/__init__.py
from flask import Blueprint

# 创建管理后台蓝图，确保名称唯一
bp = Blueprint('admin', __name__, template_folder='templates')

from . import routes