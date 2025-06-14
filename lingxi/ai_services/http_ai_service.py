from .base import BaseAIService, ProofreadingResult
from typing import Dict, Any, Optional


class HTTPAIService(BaseAIService):
    """基于HTTP请求的AI服务基类"""
    
    def __init__(self, api_key: str, base_url: str, model_name: str):
        super().__init__(api_key)
        self.base_url = base_url
        self.model_name = model_name
    
    def proofread(self, text: str) -> ProofreadingResult:
        """使用HTTP API进行文本校对"""
        try:
            prompt = self._get_proofreading_prompt(text)
            
            headers = self._get_headers()
            data = self._get_request_data(prompt)
            
            result = self._make_http_request(self.base_url, headers, data)
            result_text = self._extract_content_from_response(result)
            
            return self._parse_response(result_text)
            
        except Exception as e:
            return self._create_error_result(text, "API错误", str(e))
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _get_request_data(self, prompt: str) -> Dict[str, Any]:
        """获取请求数据"""
        return {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": self._get_system_message()},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1,
            "max_tokens": 2000
        }
    
    def _extract_content_from_response(self, response: Dict[str, Any]) -> str:
        """从响应中提取内容"""
        return response['choices'][0]['message']['content'] 