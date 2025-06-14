#!/usr/bin/env python3
"""
灵犀校对平台 - 生产环境启动脚本
使用 uv 管理依赖和虚拟环境
"""

import os
import sys
import subprocess

def check_uv():
    """检查 uv 是否已安装"""
    try:
        subprocess.run(['uv', '--version'], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def main():
    # 检查 uv 是否安装
    if not check_uv():
        print("错误: 未找到 uv 包管理器")
        print("请先安装 uv: curl -LsSf https://astral.sh/uv/install.sh | sh")
        sys.exit(1)
    
    # 检查环境变量
    required_env_vars = ['SECRET_KEY', 'ENCRYPTION_KEY']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"错误: 缺少必要的环境变量: {', '.join(missing_vars)}")
        print("请设置以下环境变量:")
        print("export SECRET_KEY='your-secret-key'")
        print("export ENCRYPTION_KEY='your-encryption-key'")
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
    print(f"启动生产服务器，端口: {port}")
    
    try:
        subprocess.run([
            'uv', 'run', 'gunicorn', 
            '--bind', f'0.0.0.0:{port}',
            '--workers', '4',
            '--timeout', '120',
            'app:app'
        ], check=True)
    except subprocess.CalledProcessError:
        print("错误: 服务启动失败")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n服务已停止")

if __name__ == '__main__':
    main() 