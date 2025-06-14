from .http_ai_service import HTTPAIService
from typing import Optional


class DeepSeekService(HTTPAIService):
    """DeepSeek服务实现"""
    
    def __init__(self, api_key: str, model: Optional[str] = None):
        super().__init__(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1/chat/completions",
            default_model="deepseek-chat",
            model=model
        ) 