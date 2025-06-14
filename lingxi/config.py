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
    
    # AI模型配置 - 每个提供商的可用模型（根据最新模型列表更新）
    AI_MODELS = {
        'openai': {
            'models': [
                {'id': 'gpt-4o', 'name': 'GPT-4o', 'description': '最新的多模态模型，强推理能力'},
                {'id': 'gpt-4-turbo', 'name': 'GPT-4 Turbo', 'description': '速度更快的GPT-4，超大上下文'},
                {'id': 'o3-mini', 'name': 'o3-mini', 'description': 'o3系列轻量版，高效推理'},
                {'id': 'o3', 'name': 'o3', 'description': 'o3系列完整版，顶级推理能力'},
                {'id': 'gpt-4', 'name': 'GPT-4', 'description': '经典强大模型，适合复杂任务'},
                {'id': 'gpt-3.5-turbo', 'name': 'GPT-3.5 Turbo', 'description': '经济实用的模型'}
            ],
            'default_model': 'gpt-4o'
        },
        'deepseek': {
            'models': [
                {'id': 'deepseek-r1', 'name': 'DeepSeek-R1', 'description': '最新推理增强模型，强化学习优化'},
                {'id': 'deepseek-r1-zero', 'name': 'DeepSeek-R1-Zero', 'description': 'R1零样本版本，无需训练数据'},
                {'id': 'deepseek-v3', 'name': 'DeepSeek-V3', 'description': 'V3系列模型，中文优化，大上下文'},
                {'id': 'deepseek-chat', 'name': 'DeepSeek Chat', 'description': '通用对话模型，中文友好'},
                {'id': 'deepseek-coder', 'name': 'DeepSeek Coder', 'description': '代码专用模型，编程任务优化'},
                {'id': 'deepseek-r1-lite-preview', 'name': 'DeepSeek R1 Lite', 'description': 'R1轻量预览版'}
            ],
            'default_model': 'deepseek-r1'
        },
        'gemini': {
            'models': [
                {'id': 'gemini-2.5-pro', 'name': 'Gemini 2.5 Pro', 'description': '最新2.5版本，多语言支持，集成搜索'},
                {'id': 'gemini-1.5-pro', 'name': 'Gemini 1.5 Pro', 'description': '高性能模型，强大推理能力'},
                {'id': 'gemini-1.5-flash', 'name': 'Gemini 1.5 Flash', 'description': '快速响应模型，平衡性能与速度'},
                {'id': 'palm-2', 'name': 'PaLM 2', 'description': '多语言大模型，集成Bard功能'},
                {'id': 'gemini-1.0-pro', 'name': 'Gemini 1.0 Pro', 'description': '稳定版本模型'}
            ],
            'default_model': 'gemini-2.5-pro'
        },
        'qwen': {
            'models': [
                {'id': 'qwen3-235b', 'name': 'Qwen3-235B', 'description': '最新Qwen3系列，2350亿参数超大模型'},
                {'id': 'qwen2.5-72b', 'name': 'Qwen2.5-72B', 'description': 'Qwen2.5系列，720亿参数，中文及多语言支持'},
                {'id': 'qwen-max', 'name': 'Qwen Max', 'description': '最强模型，顶级性能'},
                {'id': 'qwen-plus', 'name': 'Qwen Plus', 'description': '增强模型，高质量输出'},
                {'id': 'qwen-turbo', 'name': 'Qwen Turbo', 'description': '快速模型，高效响应'},
                {'id': 'qwen2.5-72b-instruct', 'name': 'Qwen2.5 72B Instruct', 'description': '指令优化版本'}
            ],
            'default_model': 'qwen3-235b'
        },
        'zhipu': {
            'models': [
                {'id': 'glm-4-flash', 'name': 'GLM-4-Flash', 'description': '闪电版GLM-4，快速响应，中文优化'},
                {'id': 'glm-4-long', 'name': 'GLM-4-Long', 'description': '长文本版GLM-4，支持超长上下文'},
                {'id': 'pangu-dialog', 'name': 'PanGu-Dialog', 'description': '盘古对话模型，中文多轮对话专用'},
                {'id': 'glm-4', 'name': 'GLM-4', 'description': '通用语言模型，中文优化'},
                {'id': 'glm-4v', 'name': 'GLM-4V', 'description': '多模态模型，支持图文理解'},
                {'id': 'glm-3-turbo', 'name': 'GLM-3 Turbo', 'description': '快速模型，经济实用'}
            ],
            'default_model': 'glm-4-flash'
        },
        'custom_openai': {
            'models': [
                {'id': 'custom-model', 'name': '自定义模型', 'description': '自定义OpenAI兼容模型'},
                {'id': 'custom-model-1', 'name': '自定义模型-1', 'description': '用户自定义模型配置'},
                {'id': 'custom-model-2', 'name': '自定义模型-2', 'description': '用户自定义模型配置'}
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
    def add_custom_model(cls, provider_key: str, model_id: str, model_name: str, description: str = '') -> bool:
        """动态添加自定义模型"""
        if provider_key not in cls.AI_MODELS:
            return False
        
        # 检查模型是否已存在
        existing_models = [m['id'] for m in cls.AI_MODELS[provider_key]['models']]
        if model_id in existing_models:
            return False
        
        # 添加新模型
        new_model = {
            'id': model_id,
            'name': model_name,
            'description': description or f'自定义{model_name}模型'
        }
        cls.AI_MODELS[provider_key]['models'].append(new_model)
        return True
    
    @classmethod
    def update_model_info(cls, provider_key: str, model_id: str, model_name: str = None, description: str = None) -> bool:
        """更新模型信息"""
        if provider_key not in cls.AI_MODELS:
            return False
        
        for model in cls.AI_MODELS[provider_key]['models']:
            if model['id'] == model_id:
                if model_name:
                    model['name'] = model_name
                if description:
                    model['description'] = description
                return True
        return False
    
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