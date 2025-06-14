#!/usr/bin/env python3
"""
灵犀校对平台 - 工具函数模块
"""

import subprocess
import os


def check_uv():
    """检查 uv 是否已安装"""
    try:
        subprocess.run(['uv', '--version'], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def run_command(cmd, description):
    """运行命令并显示描述"""
    print(f"\n🔧 {description}...")
    try:
        subprocess.run(cmd, check=True)
        print(f"✓ {description}完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description}失败: {e}")
        return False


def check_required_env_vars(required_vars):
    """检查必要的环境变量"""
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    return missing_vars


def generate_secret_key():
    """生成安全密钥"""
    import secrets
    return secrets.token_urlsafe(32) 