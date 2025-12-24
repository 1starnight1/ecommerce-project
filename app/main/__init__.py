# app/main/__init__.py
from flask import Blueprint

# 主应用蓝图
bp = Blueprint('main', __name__)

from . import routes