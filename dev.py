#!/usr/bin/env python3
"""
灵犀校对平台 - 开发工具脚本
使用 uv 管理开发任务
"""

import os
import sys
import subprocess
import argparse

# 添加 lingxi 模块到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lingxi'))
from utils import check_uv, run_command, generate_secret_key

def setup():
    """初始化开发环境"""
    if not check_uv():
        print("❌ 错误: 未找到 uv 包管理器")
        print("请先安装 uv: curl -LsSf https://astral.sh/uv/install.sh | sh")
        return False
    
    print("🚀 初始化开发环境...")
    
    # 同步依赖
    if not run_command(['uv', 'sync'], "同步依赖"):
        return False
    
    # 安装开发依赖
    if not run_command(['uv', 'sync', '--group', 'dev'], "安装开发依赖"):
        return False
    
    # 检查环境变量文件
    if not os.path.exists('.env'):
        print("\n🔑 创建环境变量文件...")
        secret_key = generate_secret_key()
        encryption_key = generate_secret_key()
        
        with open('.env', 'w') as f:
            f.write(f"SECRET_KEY={secret_key}\n")
            f.write(f"ENCRYPTION_KEY={encryption_key}\n")
            f.write("FLASK_ENV=development\n")
        
        print("✓ .env 文件已创建")
    
    # 初始化数据库
    print("\n🗄️  初始化数据库...")
    if not run_command(['uv', 'run', 'python', 'init_database.py'], "数据库初始化"):
        print("⚠️  数据库初始化失败，但可能不影响应用启动")
    
    print("\n✨ 开发环境初始化完成!")
    print("💡 运行 'python dev.py serve' 启动开发服务器")
    return True

def serve():
    """启动开发服务器"""
    print("🌟 启动开发服务器...")
    
    # 检查端口5000是否被占用
    try:
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            result = s.connect_ex(('localhost', 5000))
            if result == 0:
                print("⚠️  端口5000被占用，尝试使用端口5001...")
                os.environ['FLASK_RUN_PORT'] = '5001'
            else:
                os.environ['FLASK_RUN_PORT'] = '5000'
    except Exception:
        os.environ['FLASK_RUN_PORT'] = '5000'
    
    try:
        subprocess.run(['uv', 'run', 'python', 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n🛑 开发服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("💡 提示: 尝试运行 'python dev.py setup' 来初始化环境")

def test():
    """运行测试"""
    print("🧪 运行测试...")
    
    # 运行基础测试
    run_command(['uv', 'run', 'python', 'test_app.py'], "基础功能测试")
    
    # 如果有 pytest，运行 pytest
    try:
        subprocess.run(['uv', 'run', 'pytest', '--version'], 
                      check=True, capture_output=True)
        run_command(['uv', 'run', 'pytest', '-v'], "pytest 测试")
    except subprocess.CalledProcessError:
        print("💡 提示: 安装 pytest 以获得更好的测试体验")

def format_code():
    """格式化代码"""
    print("✨ 格式化代码...")
    
    # 使用 black 格式化
    run_command(['uv', 'run', 'black', '.'], "Black 代码格式化")
    
    # 使用 isort 排序导入
    run_command(['uv', 'run', 'isort', '.'], "isort 导入排序")

def lint():
    """代码检查"""
    print("🔍 代码检查...")
    
    # 使用 flake8 检查
    run_command(['uv', 'run', 'flake8', '.'], "flake8 代码检查")

def clean():
    """清理项目"""
    print("🧹 清理项目...")
    
    # 清理 Python 缓存
    run_command(['find', '.', '-type', 'd', '-name', '__pycache__', '-exec', 'rm', '-rf', '{}', '+'], 
                "清理 Python 缓存")
    
    # 清理 pytest 缓存
    run_command(['rm', '-rf', '.pytest_cache'], "清理 pytest 缓存")
    
    # 清理数据库文件
    run_command(['rm', '-f', '*.db', '*.sqlite3'], "清理数据库文件")

def build():
    """构建项目"""
    print("📦 构建项目...")
    run_command(['uv', 'build'], "构建项目包")

def main():
    parser = argparse.ArgumentParser(description='灵犀校对平台开发工具')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 子命令
    subparsers.add_parser('setup', help='初始化开发环境')
    subparsers.add_parser('serve', help='启动开发服务器')
    subparsers.add_parser('test', help='运行测试')
    subparsers.add_parser('format', help='格式化代码')
    subparsers.add_parser('lint', help='代码检查')
    subparsers.add_parser('clean', help='清理项目')
    subparsers.add_parser('build', help='构建项目')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'setup':
        setup()
    elif args.command == 'serve':
        serve()
    elif args.command == 'test':
        test()
    elif args.command == 'format':
        format_code()
    elif args.command == 'lint':
        lint()
    elif args.command == 'clean':
        clean()
    elif args.command == 'build':
        build()

if __name__ == '__main__':
    main() 