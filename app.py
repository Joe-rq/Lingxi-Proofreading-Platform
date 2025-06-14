#!/usr/bin/env python3
"""
灵犀校对平台 - 项目主入口
"""

import os
import sys

# 添加 lingxi 模块到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lingxi'))

# 导入主应用，使其可用于 WSGI 服务器（如 gunicorn）
from lingxi.app import app

if __name__ == '__main__':
    # 从环境变量获取端口，默认5000
    port = int(os.environ.get('FLASK_RUN_PORT', os.environ.get('PORT', 5000)))
    
    # 开发环境下直接运行
    print(f"🌟 启动开发服务器，端口: {port}")
    app.run(debug=True, host='0.0.0.0', port=port) 