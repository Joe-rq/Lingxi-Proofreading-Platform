from .base import BaseAIService, ProofreadingResult
from openai import OpenAI

class OpenAIService(BaseAIService):
    """OpenAI服务实现"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.client = OpenAI(api_key=api_key)
    
    def proofread(self, text: str) -> ProofreadingResult:
        """使用OpenAI进行文本校对"""
        try:
            prompt = self._get_proofreading_prompt(text)
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个专业的文本校对助手。请仔细检查文本中的语法、拼写、标点符号等问题，并按照指定格式返回结果。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            result_text = response.choices[0].message.content
            return self._parse_response(result_text)
            
        except Exception as e:
            return ProofreadingResult(
                corrected_text=text,
                issues=[{
                    "type": "API错误",
                    "original": "OpenAI API调用失败",
                    "corrected": "",
                    "position": "",
                    "explanation": f"错误信息: {str(e)}"
                }]
            ) 