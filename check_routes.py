from app import create_app
app = create_app()

with app.app_context():
    print("检查路由是否存在...")
    
    # 检查订单管理路由
    with app.test_request_context():
        from flask import url_for
        try:
            # 测试生成取消订单路由的URL
            url = url_for('admin.cancel_order', id=1)
            print(f"取消订单路由存在: {url}")
        except Exception as e:
            print(f"取消订单路由不存在: {e}")
        
        # 测试订单管理路由
        try:
            url = url_for('admin.order_manage')
            print(f"订单管理路由存在: {url}")
        except Exception as e:
            print(f"订单管理路由不存在: {e}")
