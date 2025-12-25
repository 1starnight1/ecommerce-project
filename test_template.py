from flask import Flask, render_template_string
import os
import sys

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 测试模板渲染
test_template = '''
<!DOCTYPE html>
<html>
<body>
    <h1>测试模板</h1>
    <p>基本模板渲染功能正常</p>
</body>
</html>
'''

def test_jinja2_template():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test'
    
    @app.route('/shop/update_cart')
    def update_cart():
        return 'Update cart'
    
    with app.test_client() as client:
        with app.app_context():
            # 渲染模板
            rendered = render_template_string(test_template)
            print("模板渲染结果:")
            print(rendered)
            print("\n✓ 模板渲染成功!")

if __name__ == '__main__':
    test_jinja2_template()
