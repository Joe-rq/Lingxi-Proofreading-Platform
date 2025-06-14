from abc import ABC, abstractmethod
from typing import Dict, List, Any

class ProofreadingResult:
    """校对结果数据类"""
    def __init__(self, corrected_text: str, issues: List[Dict[str, Any]]):
        self.corrected_text = corrected_text
        self.issues = issues

class BaseAIService(ABC):
    """AI服务基类"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    @abstractmethod
    def proofread(self, text: str) -> ProofreadingResult:
        """
        执行文本校对
        
        Args:
            text: 待校对的文本
            
        Returns:
            ProofreadingResult: 包含校对结果和问题列表
        """
        pass
    
    def _get_proofreading_prompt(self, text: str) -> str:
        """获取校对提示词"""
        return f"""
请对以下文本进行校对，找出语法错误、错别字、标点符号问题等，并提供修正建议。

请按照以下JSON格式返回结果：
{{
    "corrected_text": "修正后的完整文本",
    "issues": [
        {{
            "type": "错误类型（如：语法错误、错别字、标点符号等）",
            "original": "原始错误内容",
            "corrected": "修正后内容",
            "position": "错误位置描述",
            "explanation": "修正说明"
        }}
    ]
}}

待校对文本：
{text}
"""
    
    def _parse_response(self, response_text: str) -> ProofreadingResult:
        """解析AI返回的结果"""
        import json
        import re
        
        try:
            # 尝试从响应中提取JSON
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group()
            
            result = json.loads(response_text)
            
            corrected_text = result.get('corrected_text', '')
            issues = result.get('issues', [])
            
            return ProofreadingResult(corrected_text, issues)
            
        except (json.JSONDecodeError, AttributeError) as e:
            # 如果无法解析JSON，返回原文本和空问题列表
            return ProofreadingResult(
                corrected_text=response_text,
                issues=[{
                    "type": "解析错误",
                    "original": "无法解析AI返回结果",
                    "corrected": "",
                    "position": "",
                    "explanation": f"AI返回格式不正确: {str(e)}"
                }]
            ) 