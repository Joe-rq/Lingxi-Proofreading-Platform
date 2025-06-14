from .http_ai_service import HTTPAIService


class DeepSeekService(HTTPAIService):
    """DeepSeek服务实现"""
    
    def __init__(self, api_key: str):
        super().__init__(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1/chat/completions",
            model_name="deepseek-chat"
        ) 