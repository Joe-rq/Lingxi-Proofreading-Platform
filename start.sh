#!/bin/bash

# 灵犀校对平台 - 快速启动脚本 (使用 uv)

echo "🚀 启动灵犀校对平台..."

# 检查是否安装了 uv
if ! command -v uv &> /dev/null; then
    echo "❌ 错误: 未找到 uv 包管理器"
    echo "📦 请先安装 uv："
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "   或访问: https://github.com/astral-sh/uv"
    exit 1
fi

echo "✓ uv 已安装: $(uv --version)"

# 检查Python版本
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ 错误: 需要Python 3.9或更高版本，当前版本: $python_version"
    exit 1
fi

echo "✓ Python版本检查通过: $python_version"

# 同步依赖
echo "📚 同步依赖..."
uv sync

# 检查环境变量
if [ ! -f ".env" ]; then
    echo "⚠️  警告: 未找到.env文件，将使用默认配置"
    echo "🔑 生成默认环境变量..."
    
    # 生成随机密钥
    SECRET_KEY=$(uv run python -c "import secrets; print(secrets.token_urlsafe(32))")
    ENCRYPTION_KEY=$(uv run python -c "import secrets; print(secrets.token_urlsafe(32))")
    
    cat > .env << EOF
SECRET_KEY=$SECRET_KEY
ENCRYPTION_KEY=$ENCRYPTION_KEY
FLASK_ENV=development
EOF
    
    echo "✓ 已创建.env文件"
fi

# 初始化数据库
echo "🗄️  初始化数据库..."
uv run python init_database.py

# 检查端口5000是否被占用
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null; then
    echo "⚠️  端口5000被占用，尝试使用端口5001..."
    PORT=5001
else
    PORT=5000
fi

# 启动应用
echo "🌟 启动应用..."
echo "📱 访问地址: http://localhost:$PORT"
echo "🛑 按 Ctrl+C 停止服务"
echo ""

# 设置环境变量并启动服务器
export FLASK_RUN_PORT=$PORT
uv run python app.py 