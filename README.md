# 灵犀校对平台 (Lingxi Proofreading Platform)

一个强大、灵活且可扩展的在线文本校对平台。用户可以通过管理自己的API密钥，自由选择并利用包括OpenAI、Gemini、国产大模型乃至自托管模型在内的多种AI引擎，获得完全自定义和专业级的文本优化体验。

## ✨ 特性

- 🔒 **安全可靠**: 用户密码哈希存储，API密钥加密保存
- 🤖 **多模型支持**: 支持OpenAI、Gemini、DeepSeek、Qwen、智谱AI等多种AI模型
- 🛠️ **高度可扩展**: 采用策略模式设计，轻松添加新的AI服务提供商
- 📊 **结构化结果**: 清晰展示发现的问题和优化后的全文
- 📝 **历史记录**: 自动保存校对历史，方便回顾和管理
- 🎨 **现代UI**: 基于Bootstrap 5的响应式设计

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip

### 安装步骤

1. **安装 uv（推荐的包管理器）**
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 或者访问 https://github.com/astral-sh/uv 查看更多安装方式
```

2. **克隆项目**
```bash
git clone <repository-url>
cd 灵犀文档校对平台
```

3. **快速启动（三种方式）**

**方式一：一键启动脚本**
```bash
chmod +x start.sh
./start.sh
```

**方式二：开发工具（推荐）**
```bash
# 初始化开发环境
python dev.py setup

# 启动开发服务器
python dev.py serve
```

**方式三：手动启动**
```bash
# 同步依赖
uv sync

# 创建环境变量文件
echo "SECRET_KEY=your-secret-key-here" > .env
echo "ENCRYPTION_KEY=your-encryption-key-here" >> .env

# 运行应用
uv run python app.py
```

4. **访问应用**
打开浏览器访问 `http://localhost:5000`

## 🛠️ 开发工具

项目提供了便捷的开发工具脚本 `dev.py`：

```bash
# 查看所有可用命令
python dev.py --help

# 初始化开发环境（推荐首次使用）
python dev.py setup

# 启动开发服务器
python dev.py serve

# 运行测试
python dev.py test

# 格式化代码
python dev.py format

# 代码检查
python dev.py lint

# 清理项目文件
python dev.py clean

# 构建项目包
python dev.py build
```

## 📖 使用说明

### 1. 用户注册和登录
- 访问应用首页，点击"立即注册"创建账户
- 使用用户名和密码登录系统

### 2. 配置AI模型
- 登录后点击"设置"进入API密钥管理页面
- 选择AI服务提供商并输入您的API密钥
- 支持的服务商：
  - **OpenAI**: 需要OpenAI API密钥
  - **Google Gemini**: 需要Google AI API密钥
  - **DeepSeek**: 需要DeepSeek API密钥
  - **Qwen**: 需要阿里云通义千问API密钥
  - **智谱AI**: 需要智谱AI API密钥
  - **Custom OpenAI**: 支持自定义OpenAI兼容API

### 3. 开始校对
- 返回首页，选择已配置的AI模型
- 在文本框中输入待校对的文本
- 点击"开始校对"按钮
- 查看校对结果，包括发现的问题列表和优化后的全文

### 4. 查看历史
- 点击"历史记录"查看所有校对历史
- 可以复制历史记录中的校对结果

## 🔧 技术栈

- **包管理**: uv (现代 Python 包管理器)
- **后端**: Flask + SQLAlchemy + Flask-Login
- **数据库**: SQLite (开发环境) / PostgreSQL (生产环境)
- **前端**: HTML5 + CSS3 + JavaScript + Bootstrap 5
- **安全**: Werkzeug (密码哈希) + cryptography (API密钥加密)
- **AI集成**: OpenAI SDK + requests (其他AI服务)

## 📁 项目结构

```
灵犀校对平台/
├── lingxi/                  # 应用主目录
│   ├── pycache/             # Python缓存
│   ├── ai_services/         # AI服务模块
│   │   ├── pycache/
│   │   ├── __init__.py
│   │   ├── base.py          # 基类
│   │   ├── openai_service.py
│   │   ├── gemini_service.py
│   │   ├── deepseek_service.py
│   │   ├── qwen_service.py
│   │   ├── zhipu_service.py
│   │   └── custom_openai_service.py
│   ├── templates/           # HTML模板
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── index.html
│   │   ├── settings.html
│   │   ├── history.html
│   │   ├── 404.html
│   │   └── 500.html
│   ├── static/              # 静态文件
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   ├── __init__.py          # 包初始化文件
│   ├── app.py               # Flask应用路由和视图
│   ├── config.py            # 应用配置，包含模型定义
│   ├── models.py            # 数据库模型
│   ├── helpers.py           # 辅助函数
│   ├── utils.py             # 工具函数
│   └── logging_config.py    # 日志配置
├── instance/                # 实例文件夹，用于存放数据库等
├── .venv/                   # Python虚拟环境
├── tests/                   # 测试目录
├── doc/                     # 文档目录
├── .git/                    # Git目录
├── .gitignore               # Git忽略配置
├── app.py                   # 入口文件（兼容旧版）
├── dev.py                   # 开发工具脚本
├── run.py                   # 生产环境启动脚本
├── init_database.py         # 数据库初始化脚本
├── requirements.txt         # Python依赖（备用）
├── pyproject.toml           # uv项目配置和依赖
├── uv.lock                  # uv锁定文件
├── start.sh                 # 一键启动脚本
├── LICENSE                  # 开源许可证
└── README.md                # 项目说明
```

## 🔒 安全特性

1. **密码安全**: 使用Werkzeug的密码哈希功能
2. **API密钥加密**: 使用cryptography库加密存储用户API密钥
3. **环境变量**: 敏感配置通过环境变量管理
4. **用户会话**: Flask-Login管理用户认证状态

## 🚀 部署

### 生产环境部署

1. **使用 uv 和 Gunicorn**
```bash
# 安装生产依赖
uv sync

# 设置环境变量
export SECRET_KEY="your-secret-key"
export ENCRYPTION_KEY="your-encryption-key"
export FLASK_ENV="production"

# 使用 Gunicorn 启动
uv run gunicorn --bind 0.0.0.0:5000 app:app
```

2. **配置 Nginx 反向代理**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

3. **使用 PostgreSQL 数据库**
```bash
# 设置数据库URL
export DATABASE_URL="postgresql://user:password@localhost/lingxi_proofreading"
```

## 🤝 贡献

欢迎提交问题和改进建议！

## 📄 许可证

MIT License

## 📧 联系方式

如有问题请提交Issue或联系开发者。

---

**注意**: 请确保妥善保管您的API密钥，不要在公共场所或代码中暴露这些敏感信息。 