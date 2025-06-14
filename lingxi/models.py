from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
from datetime import datetime
import base64
import hashlib
import json

db = SQLAlchemy()

class CryptoHelper:
    """用于加密和解密API密钥的助手类"""
    
    @staticmethod
    def _get_key(password: str) -> bytes:
        """从密码生成加密密钥"""
        return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())
    
    @staticmethod
    def encrypt_api_key(api_key: str, encryption_password: str) -> str:
        """加密API密钥"""
        key = CryptoHelper._get_key(encryption_password)
        fernet = Fernet(key)
        encrypted_key = fernet.encrypt(api_key.encode())
        return base64.urlsafe_b64encode(encrypted_key).decode()
    
    @staticmethod
    def decrypt_api_key(encrypted_api_key: str, encryption_password: str) -> str:
        """解密API密钥"""
        key = CryptoHelper._get_key(encryption_password)
        fernet = Fernet(key)
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_api_key.encode())
        decrypted_key = fernet.decrypt(encrypted_bytes)
        return decrypted_key.decode()

class User(UserMixin, db.Model):
    """用户模型"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联关系
    api_keys = db.relationship('APIKey', backref='user', lazy=True, cascade='all, delete-orphan')
    proofreading_history = db.relationship('ProofreadingHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """设置密码（哈希存储）"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def get_available_models(self):
        """获取用户可用的所有模型"""
        from config import Config
        available_models = []
        
        for api_key in self.api_keys:
            provider_models = Config.get_provider_models(api_key.provider)
            provider_name = Config.get_provider_name(api_key.provider)
            
            for model in provider_models.get('models', []):
                available_models.append({
                    'provider': api_key.provider,
                    'provider_name': provider_name,
                    'model_id': model['id'],
                    'model_name': model['name'],
                    'description': model['description'],
                    'full_name': f"{provider_name} - {model['name']}"
                })
        
        return available_models
    
    def __repr__(self):
        return f'<User {self.username}>'

class APIKey(db.Model):
    """API密钥模型"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    provider = db.Column(db.String(50), nullable=False)  # openai, gemini, deepseek, etc.
    encrypted_api_key = db.Column(db.Text, nullable=False)
    base_url = db.Column(db.String(200))  # 用于custom_openai
    enabled_models = db.Column(db.Text)  # JSON格式存储启用的模型列表
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_api_key(self, api_key: str, encryption_password: str):
        """设置加密的API密钥"""
        self.encrypted_api_key = CryptoHelper.encrypt_api_key(api_key, encryption_password)
    
    def get_api_key(self, encryption_password: str) -> str:
        """获取解密的API密钥"""
        return CryptoHelper.decrypt_api_key(self.encrypted_api_key, encryption_password)
    
    def set_enabled_models(self, model_ids: list):
        """设置启用的模型列表"""
        if model_ids:
            self.enabled_models = json.dumps(model_ids)
        else:
            self.enabled_models = None
    
    def get_enabled_models(self) -> list:
        """获取启用的模型列表"""
        if self.enabled_models:
            try:
                return json.loads(self.enabled_models)
            except json.JSONDecodeError:
                return []
        return []
    
    def get_available_models(self):
        """获取此API密钥可用的模型"""
        from config import Config
        provider_models = Config.get_provider_models(self.provider)
        enabled_models = self.get_enabled_models()
        
        # 如果没有设置启用的模型，返回所有模型
        if not enabled_models:
            return provider_models.get('models', [])
        
        # 返回启用的模型
        available = []
        for model in provider_models.get('models', []):
            if model['id'] in enabled_models:
                available.append(model)
        
        return available
    
    def __repr__(self):
        return f'<APIKey {self.provider} for User {self.user_id}>'

class ProofreadingHistory(db.Model):
    """校对历史模型"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    original_text = db.Column(db.Text, nullable=False)
    corrected_text = db.Column(db.Text, nullable=False)
    issues_found = db.Column(db.Text)  # JSON格式存储发现的问题
    provider_used = db.Column(db.String(50), nullable=False)  # AI提供商
    model_used = db.Column(db.String(100), nullable=False)  # 具体模型
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_model_display_name(self):
        """获取模型的显示名称"""
        from config import Config
        provider_name = Config.get_provider_name(self.provider_used)
        model_info = Config.get_model_info(self.provider_used, self.model_used)
        
        if model_info:
            return f"{provider_name} - {model_info['name']}"
        else:
            return f"{provider_name} - {self.model_used}"
    
    def __repr__(self):
        return f'<ProofreadingHistory {self.id} by User {self.user_id}>' 