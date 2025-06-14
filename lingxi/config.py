import os
from dotenv import load_dotenv

load_dotenv()

class Config:
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