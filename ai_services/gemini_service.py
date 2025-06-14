from .base import BaseAIService, ProofreadingResult
import google.generativeai as genai

class GeminiService(BaseAIService):
    """Google Gemini服务实现"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def proofread(self, text: str) -> ProofreadingResult:
        """使用Gemini进行文本校对"""
        try:
            prompt = self._get_proofreading_prompt(text)
            
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,
                    max_output_tokens=2000
                )
            )
            
            result_text = response.text
            return self._parse_response(result_text)
            
        except Exception as e:
            return ProofreadingResult(
                corrected_text=text,
                issues=[{
                    "type": "API错误",
                    "original": "Gemini API调用失败",
                    "corrected": "",
                    "position": "",
                    "explanation": f"错误信息: {str(e)}"
                }]
            ) 