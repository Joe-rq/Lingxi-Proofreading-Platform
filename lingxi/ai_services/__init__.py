from .base import BaseAIService, ProofreadingResult
from .http_ai_service import HTTPAIService
from .openai_service import OpenAIService
from .gemini_service import GeminiService
from .deepseek_service import DeepSeekService
from .qwen_service import QwenService
from .zhipu_service import ZhipuService
from .custom_openai_service import CustomOpenAIService

# AI服务工厂
AI_SERVICES = {
    'openai': OpenAIService,
    'gemini': GeminiService,
    'deepseek': DeepSeekService,
    'qwen': QwenService,
    'zhipu': ZhipuService,
    'custom_openai': CustomOpenAIService
}

def get_ai_service(provider: str, api_key: str, base_url: str = None) -> BaseAIService:
    """获取AI服务实例"""
    if provider not in AI_SERVICES:
        raise ValueError(f"Unsupported AI provider: {provider}")
    
    service_class = AI_SERVICES[provider]
    
    if provider == 'custom_openai':
        return service_class(api_key, base_url)
    else:
        return service_class(api_key) 