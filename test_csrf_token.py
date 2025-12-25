from app import create_app
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = create_app()

with app.test_client() as client:
    # 获取登录页面以获取CSRF令牌
    login_page_response = client.get('/auth/login')
    logger.info(f"获取登录页面状态码: {login_page_response.status_code}")
    
    # 提取登录页面的CSRF令牌
    login_page_content = login_page_response.data.decode('utf-8')
    import re
    login_csrf = re.search(r'<input.*?name="csrf_token".*?value="([^"]+)"', login_page_content)
    if login_csrf:
        login_csrf_token = login_csrf.group(1)
        logger.info(f"登录页面CSRF令牌: {login_csrf_token}")
        
        # 登录管理员
        login_response = client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123',
            'csrf_token': login_csrf_token
        })
        logger.info(f"登录状态码: {login_response.status_code}")
    else:
        logger.error("❌ 无法获取登录页面CSRF令牌")
    
    # 获取订单管理页面
    order_manage_response = client.get('/admin/orders')
    logger.info(f"获取订单管理页面状态码: {order_manage_response.status_code}")
    
    # 检查页面内容
    page_content = order_manage_response.data.decode('utf-8')
    
    # 查找取消订单表单
    import re
    cancel_form_pattern = r'<form method="POST" action="/admin/orders/\d+/cancel".*?</form>'
    cancel_forms = re.findall(cancel_form_pattern, page_content, re.DOTALL)
    
    if cancel_forms:
        logger.info(f"找到 {len(cancel_forms)} 个取消订单表单")
        for i, form in enumerate(cancel_forms):
            logger.info(f"表单 {i+1} 内容:")
            logger.info(form)
            
            # 检查是否包含CSRF令牌
            if '{{ csrf_token() }}' in form:
                logger.error("❌ CSRF令牌函数未被渲染，仍为模板语法")
            else:
                csrf_input = re.search(r'<input.*?name="csrf_token".*?value="([^"]+)"', form)
                if csrf_input:
                    logger.info(f"✅ 找到CSRF令牌: {csrf_input.group(1)}")
                else:
                    logger.error("❌ 表单中没有CSRF令牌")
    else:
        logger.error("❌ 未找到取消订单表单")
        # 输出页面的一部分来调试
        logger.info("页面内容预览:")
        logger.info(page_content[:2000])