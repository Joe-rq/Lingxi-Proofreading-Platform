#!/usr/bin/env python3
"""
灵犀校对平台 - 生产环境启动脚本
使用 uv 管理依赖和虚拟环境
"""

import os
import sys
import subprocess

# 添加 lingxi 模块到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lingxi'))
from utils import check_uv, check_required_env_vars


def main():
    # 检查 uv 是否安装
    if not check_uv():
        print("错误: 未找到 uv 包管理器")
        print("请先安装 uv: curl -LsSf https://astral.sh/uv/install.sh | sh")
        sys.exit(1)
    
    # 检查环境变量
    required_env_vars = ['SECRET_KEY', 'ENCRYPTION_KEY']
    missing_vars = check_required_env_vars(required_env_vars)
    
    if missing_vars:
        print(f"错误: 缺少必要的环境变量: {', '.join(missing_vars)}")
        print("请设置以下环境变量:")
        for var in missing_vars:
            print(f"export {var}='your-{var.lower().replace('_', '-')}'")
        sys.exit(1)
    
    # 同步依赖
    print("同步依赖...")
    try:
        subprocess.run(['uv', 'sync'], check=True)
    except subprocess.CalledProcessError:
        print("错误: 依赖同步失败")
        sys.exit(1)
    
    # 设置生产环境配置
    os.environ['FLASK_ENV'] = 'production'
    
    # 启动应用
    port = int(os.environ.get('PORT', 5000))
    workers = int(os.environ.get('WORKERS', 4))
    timeout = int(os.environ.get('TIMEOUT', 120))
    
    print(f"启动生产服务器，端口: {port}, 工作进程: {workers}")
    
    try:
        subprocess.run([
            'uv', 'run', 'gunicorn', 
            '--bind', f'0.0.0.0:{port}',
            '--workers', str(workers),
            '--timeout', str(timeout),
            'app:app'  # 直接使用根目录的app.py
        ], check=True)
    except subprocess.CalledProcessError:
        print("错误: 服务启动失败")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n服务已停止")


if __name__ == '__main__':
    main() 