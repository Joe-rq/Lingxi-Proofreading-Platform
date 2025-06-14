#!/usr/bin/env python3
"""
灵犀校对平台 - 基础测试脚本
使用 uv 运行测试
"""

import os
import sys
import tempfile
import unittest
import subprocess

def check_uv():
    """检查 uv 是否已安装"""
    try:
        subprocess.run(['uv', '--version'], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

# 确保可以导入应用模块
if check_uv():
    # 使用 uv 运行时，模块应该在正确的环境中
    pass
else:
    print("警告: 未找到 uv，使用系统 Python 运行测试")

from app import app, db
from models import User, APIKey

class LingxiTestCase(unittest.TestCase):
    """基础测试用例"""
    
    def setUp(self):
        """测试前准备"""
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        """测试后清理"""
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
    
    def test_home_redirect(self):
        """测试首页重定向到登录"""
        rv = self.app.get('/')
        assert rv.status_code == 302
        assert '/login' in rv.location
    
    def test_login_page(self):
        """测试登录页面"""
        rv = self.app.get('/login')
        assert rv.status_code == 200
        assert '用户登录' in rv.data.decode('utf-8')
    
    def test_register_page(self):
        """测试注册页面"""
        rv = self.app.get('/register')
        assert rv.status_code == 200
        assert '用户注册' in rv.data.decode('utf-8')
    
    def test_user_registration(self):
        """测试用户注册"""
        rv = self.app.post('/register', data={
            'username': 'testuser',
            'password': 'testpass123'
        }, follow_redirects=True)
        assert rv.status_code == 200
        assert '注册成功' in rv.data.decode('utf-8')
    
    def test_user_login(self):
        """测试用户登录"""
        # 先注册用户
        with app.app_context():
            user = User(username='testuser')
            user.set_password('testpass123')
            db.session.add(user)
            db.session.commit()
        
        # 测试登录
        rv = self.app.post('/login', data={
            'username': 'testuser',
            'password': 'testpass123'
        }, follow_redirects=True)
        assert rv.status_code == 200
    
    def test_password_hashing(self):
        """测试密码哈希"""
        with app.app_context():
            user = User(username='testuser')
            user.set_password('testpass123')
            
            # 密码应该被哈希
            assert user.password_hash != 'testpass123'
            
            # 密码验证应该正确
            assert user.check_password('testpass123')
            assert not user.check_password('wrongpass')
    
    def test_api_key_encryption(self):
        """测试API密钥加密"""
        with app.app_context():
            user = User(username='testuser')
            user.set_password('testpass123')
            db.session.add(user)
            db.session.commit()
            
            api_key = APIKey(user_id=user.id, provider='openai')
            original_key = 'sk-test1234567890'
            api_key.set_api_key(original_key, app.config['ENCRYPTION_KEY'])
            
            # 密钥应该被加密
            assert api_key.encrypted_api_key != original_key
            
            # 解密应该正确
            decrypted_key = api_key.get_api_key(app.config['ENCRYPTION_KEY'])
            assert decrypted_key == original_key

def test_ai_services():
    """测试AI服务模块"""
    from ai_services import get_ai_service
    from ai_services.base import ProofreadingResult
    
    # 测试工厂函数
    try:
        service = get_ai_service('openai', 'test-key')
        assert service is not None
        print("✓ AI服务工厂函数正常")
    except Exception as e:
        print(f"✗ AI服务工厂函数错误: {e}")
    
    # 测试不支持的提供商
    try:
        get_ai_service('unsupported', 'test-key')
        print("✗ 应该抛出异常")
    except ValueError:
        print("✓ 不支持的提供商异常处理正常")

def run_tests_with_uv():
    """使用 uv 运行测试"""
    if not check_uv():
        print("错误: 未找到 uv 包管理器")
        print("请先安装 uv: curl -LsSf https://astral.sh/uv/install.sh | sh")
        return False
    
    try:
        print("使用 uv 运行测试...")
        result = subprocess.run([
            'uv', 'run', 'python', '-m', 'pytest', 'test_app.py', '-v'
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
            
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("灵犀校对平台 - 基础功能测试")
    print("=" * 50)
    
    # 首先尝试使用 uv 运行 pytest
    if check_uv():
        print("\n使用 uv 环境运行测试...")
        if run_tests_with_uv():
            print("✓ uv pytest 测试通过")
        else:
            print("⚠️ uv pytest 测试失败，回退到 unittest")
    
    # 运行单元测试
    print("\n1. 运行单元测试...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # 测试AI服务
    print("\n2. 测试AI服务模块...")
    test_ai_services()
    
    print("\n" + "=" * 50)
    print("测试完成!")
    print("💡 提示: 可以运行 'uv run pytest' 获得更好的测试体验")
    print("=" * 50)

if __name__ == '__main__':
    main() 