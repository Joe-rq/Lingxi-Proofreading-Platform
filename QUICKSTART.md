# 灵犀文档校对平台 - 快速启动指南

## 🚀 启动方式

### 方式一：使用启动脚本（推荐）
```bash
chmod +x start.sh  # 首次运行需要添加执行权限
./start.sh
```

### 方式二：使用开发工具
```bash
# 初始化环境（首次运行）
python dev.py setup

# 启动开发服务器
python dev.py serve
```

### 方式三：直接运行
```bash
# 同步依赖
uv sync

# 初始化数据库
uv run python init_database.py

# 启动应用
uv run python app.py
```

## 🔧 生产环境部署
```bash
# 设置环境变量
export SECRET_KEY="your-secret-key"
export ENCRYPTION_KEY="your-encryption-key"
export FLASK_ENV="production"
export PORT=8000  # 可选，指定端口

# 启动生产服务器
python run.py
```

## 🐛 故障排除

### 问题：端口5000被占用
**现象**：显示 "Address already in use" 或 "Port 5000 is in use"

**解决方案**：
1. **自动解决**：脚本会自动尝试使用端口5001
2. **手动指定端口**：
   ```bash
   export FLASK_RUN_PORT=5002
   ./start.sh
   ```
3. **macOS用户**：禁用AirPlay Receiver
   - 系统设置 → 通用 → 隔空播放与接力 → 隔空播放接收器 → 关闭

### 问题：找不到 app.py 文件
**解决方案**：确保在项目根目录运行启动命令

### 问题：ModuleNotFoundError 或 ImportError
**解决方案**：
```bash
# 重新同步依赖
uv sync

# 或者重新初始化环境
python dev.py setup
```

### 问题：数据库初始化失败
**解决方案**：
```bash
# 手动初始化数据库
uv run python init_database.py

# 或者删除旧数据库文件重新创建
rm -f *.db
./start.sh
```

### 问题：权限错误
**解决方案**：给启动脚本添加执行权限：
```bash
chmod +x start.sh
```

### 问题：uv 命令未找到
**解决方案**：安装 uv 包管理器：
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# 或者
pip install uv
```

## 📱 访问应用
启动成功后，在浏览器中访问：
- 默认地址：http://localhost:5000
- 如果端口被占用：http://localhost:5001

## 💡 开发提示
- 使用 `python dev.py --help` 查看所有可用命令
- 使用 `python dev.py clean` 清理项目
- 使用 `python dev.py format` 格式化代码
- 使用 `python dev.py lint` 检查代码质量 