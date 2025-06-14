from .base import BaseAIService, ProofreadingResult
import requests
import json

class QwenService(BaseAIService):
    """阿里云通义千问服务实现"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    
    def proofread(self, text: str) -> ProofreadingResult:
        """使用Qwen进行文本校对"""
        try:
            prompt = self._get_proofreading_prompt(text)
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "qwen-turbo",
                "input": {
                    "messages": [
                        {"role": "system", "content": "你是一个专业的文本校对助手。请仔细检查文本中的语法、拼写、标点符号等问题，并按照指定格式返回结果。"},
                        {"role": "user", "content": prompt}
                    ]
                },
                "parameters": {
                    "temperature": 0.1,
                    "max_tokens": 2000
                }
            }
            
            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            result_text = result['output']['choices'][0]['message']['content']
            return self._parse_response(result_text)
            
        except Exception as e:
            return ProofreadingResult(
                corrected_text=text,
                issues=[{
                    "type": "API错误",
                    "original": "Qwen API调用失败",
                    "corrected": "",
                    "position": "",
                    "explanation": f"错误信息: {str(e)}"
                }]
            ) 