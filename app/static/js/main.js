// 电商平台通用JavaScript功能

// DOM加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化购物车功能
    initCartFunctions();
    
    // 初始化产品图片预览
    initProductImagePreview();
    
    // 初始化表单提交功能
    initFormSubmission();
    
    // 初始化搜索功能
    initSearchFunction();
});

// 购物车功能
function initCartFunctions() {
    // 更新购物车数量
    const updateCartLinks = document.querySelectorAll('.update-cart');
    updateCartLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            // 购物车更新功能已在cart.html中通过AJAX实现
        });
    });
    
    // 删除购物车项目
    const removeCartItemLinks = document.querySelectorAll('.remove-cart-item');
    removeCartItemLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            // 确认删除
            if (confirm('确定要删除该商品吗？')) {
                window.location.href = this.getAttribute('href');
            }
        });
    });
}

// 产品图片预览
function initProductImagePreview() {
    const productImages = document.querySelectorAll('.product-image');
    productImages.forEach(img => {
        img.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
            this.style.transition = 'transform 0.3s ease';
        });
        
        img.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
}

// 表单提交功能
function initFormSubmission() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // 添加加载状态
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 处理中...';
            }
        });
    });
}

// 搜索功能
function initSearchFunction() {
    const searchInput = document.querySelector('input[name="q"]');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                // 搜索功能已通过表单提交实现
            }
        });
    }
}

// 通用功能：显示消息
function showMessage(message, type = 'success') {
    // 创建消息元素
    const messageDiv = document.createElement('div');
    messageDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-50 start-50 translate-middle`;
    messageDiv.role = 'alert';
    messageDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // 添加到页面
    document.body.appendChild(messageDiv);
    
    // 3秒后自动关闭
    setTimeout(() => {
        if (messageDiv.parentNode) {
            messageDiv.parentNode.removeChild(messageDiv);
        }
    }, 3000);
}

// 通用功能：更新购物车数量徽章
function updateCartBadge(count) {
    const cartBadge = document.getElementById('cart-badge');
    if (cartBadge) {
        cartBadge.textContent = count;
        // 如果数量为0，隐藏徽章
        if (count === 0) {
            cartBadge.style.display = 'none';
        } else {
            cartBadge.style.display = 'inline-block';
        }
    }
}

// 通用功能：格式化价格
function formatPrice(price) {
    return '¥' + parseFloat(price).toFixed(2);
}

// 通用功能：数字输入验证
function validateNumberInput(input) {
    const value = input.value;
    if (isNaN(value) || value < 1) {
        input.value = 1;
    }
}
