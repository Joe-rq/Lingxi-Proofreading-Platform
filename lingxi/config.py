import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """应用配置类"""
    
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///lingxi_proofreading.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 用于加密API密钥的密钥
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY') or 'default-encryption-key-change-in-production'
    
    # AI服务配置
    SUPPORTED_PROVIDERS = {
        'openai': 'OpenAI',
        'gemini': 'Google Gemini',
        'deepseek': 'DeepSeek',
        'qwen': 'Qwen',
        'zhipu': '智谱AI',
        'custom_openai': 'Custom OpenAI'
    }
    
    # 应用配置
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    MAX_TEXT_LENGTH = int(os.environ.get('MAX_TEXT_LENGTH', 10000))  # 10000 字符
    ITEMS_PER_PAGE = int(os.environ.get('ITEMS_PER_PAGE', 10))
    
    # 日志配置
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/app.log')
    
    # 安全配置
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    @classmethod
    def get_provider_name(cls, provider_key: str) -> str:
        """获取提供商显示名称"""
        return cls.SUPPORTED_PROVIDERS.get(provider_key, provider_key)
    
    @classmethod
    def is_production(cls) -> bool:
        """检查是否为生产环境"""
        return os.environ.get('FLASK_ENV') == 'production'
    
    @classmethod
    def validate_required_env_vars(cls) -> list[str]:
        """验证必需的环境变量"""
        required_vars = ['SECRET_KEY', 'ENCRYPTION_KEY']
        missing_vars = []
        
        for var in required_vars:
            value = os.environ.get(var)
            if not value or (var in ['SECRET_KEY', 'ENCRYPTION_KEY'] and (value.startswith('dev-') or value.startswith('default-'))):
                missing_vars.append(var)
        
        return missing_vars 