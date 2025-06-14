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
    
    # AI模型配置 - 每个提供商的可用模型
    AI_MODELS = {
        'openai': {
            'models': [
                {'id': 'gpt-3.5-turbo', 'name': 'GPT-3.5 Turbo', 'description': '经济实用的模型'},
                {'id': 'gpt-4', 'name': 'GPT-4', 'description': '更强大的模型'},
                {'id': 'gpt-4-turbo', 'name': 'GPT-4 Turbo', 'description': '速度更快的GPT-4'},
                {'id': 'gpt-4o', 'name': 'GPT-4o', 'description': '最新的多模态模型'}
            ],
            'default_model': 'gpt-3.5-turbo'
        },
        'deepseek': {
            'models': [
                {'id': 'deepseek-chat', 'name': 'DeepSeek Chat', 'description': '通用对话模型'},
                {'id': 'deepseek-coder', 'name': 'DeepSeek Coder', 'description': '代码专用模型'},
                {'id': 'deepseek-r1', 'name': 'DeepSeek R1', 'description': '推理增强模型'},
                {'id': 'deepseek-r1-lite-preview', 'name': 'DeepSeek R1 Lite', 'description': 'R1轻量版模型'}
            ],
            'default_model': 'deepseek-chat'
        },
        'gemini': {
            'models': [
                {'id': 'gemini-1.5-flash', 'name': 'Gemini 1.5 Flash', 'description': '快速响应模型'},
                {'id': 'gemini-1.5-pro', 'name': 'Gemini 1.5 Pro', 'description': '高性能模型'},
                {'id': 'gemini-1.0-pro', 'name': 'Gemini 1.0 Pro', 'description': '稳定版本模型'}
            ],
            'default_model': 'gemini-1.5-flash'
        },
        'qwen': {
            'models': [
                {'id': 'qwen-turbo', 'name': 'Qwen Turbo', 'description': '快速模型'},
                {'id': 'qwen-plus', 'name': 'Qwen Plus', 'description': '增强模型'},
                {'id': 'qwen-max', 'name': 'Qwen Max', 'description': '最强模型'},
                {'id': 'qwen2.5-72b-instruct', 'name': 'Qwen2.5 72B', 'description': '72B参数模型'}
            ],
            'default_model': 'qwen-turbo'
        },
        'zhipu': {
            'models': [
                {'id': 'glm-4', 'name': 'GLM-4', 'description': '通用语言模型'},
                {'id': 'glm-4v', 'name': 'GLM-4V', 'description': '多模态模型'},
                {'id': 'glm-3-turbo', 'name': 'GLM-3 Turbo', 'description': '快速模型'}
            ],
            'default_model': 'glm-4'
        },
        'custom_openai': {
            'models': [
                {'id': 'custom-model', 'name': '自定义模型', 'description': '自定义OpenAI兼容模型'}
            ],
            'default_model': 'custom-model'
        }
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
    def get_provider_models(cls, provider_key: str) -> dict:
        """获取指定提供商的模型列表"""
        return cls.AI_MODELS.get(provider_key, {'models': [], 'default_model': ''})
    
    @classmethod
    def get_all_models(cls) -> dict:
        """获取所有提供商的模型配置"""
        return cls.AI_MODELS
    
    @classmethod
    def get_model_info(cls, provider_key: str, model_id: str) -> dict:
        """获取特定模型的信息"""
        provider_models = cls.get_provider_models(provider_key)
        for model in provider_models.get('models', []):
            if model['id'] == model_id:
                return model
        return {}
    
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