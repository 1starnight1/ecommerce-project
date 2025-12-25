#!/bin/bash

# 电子商务网站一键部署脚本
# 解决Docker镜像拉取超时问题并实现自动化部署

set -e

# 彩色输出函数
red() { echo -e "\033[31m$1\033[0m"; }
green() { echo -e "\033[32m$1\033[0m"; }
yellow() { echo -e "\033[33m$1\033[0m"; }
blue() { echo -e "\033[34m$1\033[0m"; }

# 检查是否以root用户执行
if [ "$EUID" -ne 0 ]; then
  red "❌ 请以root用户执行此脚本 (sudo $0)"
  exit 1
fi

echo ""
green "🚀 电子商务网站一键部署脚本"
echo ""

# 步骤1：配置Docker镜像源
step=1
echo "$(yellow "[$step]") 配置Docker国内镜像源..."

# 创建Docker配置目录
mkdir -p /etc/docker

# 配置国内镜像源（阿里云专属镜像源优先）
cat > /etc/docker/daemon.json << EOF
{
  "registry-mirrors": [
    "https://zou5v96f.mirror.aliyuncs.com",
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com"
  ]
}
EOF

# 重启Docker服务
echo "$(yellow "[$step]") 重启Docker服务..."
systemctl daemon-reload
systemctl restart docker

echo "$(green "[$step]") Docker镜像源配置完成！"
echo ""

# 步骤2：清理Docker资源
step=$((step+1))
echo "$(yellow "[$step]") 清理Docker资源..."

# 进入项目目录
PROJECT_DIR="/var/www/ecommerce"
if [ -d "$PROJECT_DIR" ]; then
  cd "$PROJECT_DIR"
  echo "$(yellow "[$step]") 进入项目目录: $PROJECT_DIR"
else
  red "❌ 项目目录不存在: $PROJECT_DIR"
  exit 1
fi

# 停止并删除所有容器、网络和卷
echo "$(yellow "[$step]") 停止并删除所有容器、网络和卷..."
docker-compose down -v 2>/dev/null || echo "$(yellow "[$step]") 没有运行的compose服务"

# 删除所有容器
echo "$(yellow "[$step]") 删除所有容器..."
CONTAINERS=$(docker ps -aq 2>/dev/null || true)
if [ -n "$CONTAINERS" ]; then
  docker rm -f $CONTAINERS
  echo "$(green "[$step]") 已删除所有容器"
else
  echo "$(blue "[$step]") 没有容器需要删除"
fi

# 删除所有自定义网络
echo "$(yellow "[$step]") 删除所有自定义网络..."
NETWORKS=$(docker network ls --filter "type=custom" -q 2>/dev/null || true)
if [ -n "$NETWORKS" ]; then
  docker network rm $NETWORKS
  echo "$(green "[$step]") 已删除所有自定义网络"
else
  echo "$(blue "[$step]") 没有自定义网络需要删除"
fi

# 删除所有卷
echo "$(yellow "[$step]") 删除所有卷..."
VOLUMES=$(docker volume ls -q 2>/dev/null || true)
if [ -n "$VOLUMES" ]; then
  docker volume rm $VOLUMES
  echo "$(green "[$step]") 已删除所有卷"
else
  echo "$(blue "[$step]") 没有卷需要删除"
fi

# 清理Docker系统资源
echo "$(yellow "[$step]") 清理Docker系统资源..."
docker system prune -af --volumes

echo "$(green "[$step]") Docker资源清理完成！"
echo ""

# 步骤3：启动服务
step=$((step+1))
echo "$(yellow "[$step]") 启动Docker Compose服务..."

# 启动服务
docker-compose up -d

# 等待服务启动
echo "$(yellow "[$step]") 等待服务启动（10秒）..."
sleep 10

echo "$(green "[$step]") 服务启动完成！"
echo ""

# 步骤4：验证服务状态
step=$((step+1))
echo "$(yellow "[$step]") 验证服务状态..."

# 查看容器状态
echo "$(yellow "[$step]") 容器状态："
docker-compose ps

echo ""

# 检查网站访问
echo "$(yellow "[$step]") 测试网站访问..."
HTTP_STATUS=$(curl -o /dev/null -s -w "%{http_code}" http://localhost 2>/dev/null || echo "000")
if [ "$HTTP_STATUS" -eq 200 ]; then
  green "✅ 网站访问正常（HTTP状态码：$HTTP_STATUS）"
else
  red "❌ 网站访问失败（HTTP状态码：$HTTP_STATUS）"
  echo "$(yellow "[$step]") 查看详细日志：docker-compose logs -f"
fi

echo ""

# 完成信息
green "🎉 一键部署完成！"
echo ""
yellow "📋 后续操作："
echo "   1. 查看详细日志：docker-compose logs -f"
echo "   2. 访问网站：http://您的服务器IP"
echo "   3. 管理数据库：docker exec -it ecommerce_db mysql -u ecommerce_user -ppassword123 ecommerce"
echo ""
green "祝使用愉快！"
echo ""