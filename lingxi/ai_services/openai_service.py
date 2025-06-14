from .base import BaseAIService, ProofreadingResult
from openai import OpenAI
from typing import Optional


class OpenAIService(BaseAIService):
    """OpenAI服务实现"""
    
    def __init__(self, api_key: str, model: Optional[str] = None):
        super().__init__(api_key, model=model)
        self.client = OpenAI(api_key=api_key)
    
    def get_default_model(self) -> str:
        """获取默认模型"""
        return "gpt-3.5-turbo"
    
    def proofread(self, text: str) -> ProofreadingResult:
        """使用OpenAI进行文本校对"""
        try:
            prompt = self._get_proofreading_prompt(text)
            
            response = self.client.chat.completions.create(
                model=self.get_model(),
                messages=[
                    {"role": "system", "content": self._get_system_message()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            result_text = response.choices[0].message.content
            return self._parse_response(result_text)
            
        except Exception as e:
            return self._create_error_result(text, "API错误", str(e)) 