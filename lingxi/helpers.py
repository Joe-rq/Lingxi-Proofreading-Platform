"""
灵犀校对平台 - 辅助函数模块
"""

from flask import flash, redirect, url_for
from functools import wraps
import logging

logger = logging.getLogger(__name__)


def handle_database_operation(operation, success_message: str, error_message: str, redirect_url: str = None):
    """
    处理数据库操作的通用装饰器
    
    Args:
        operation: 要执行的数据库操作函数
        success_message: 成功时的提示消息
        error_message: 失败时的提示消息
        redirect_url: 操作完成后重定向的URL
    """
    from models import db
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = operation()
                db.session.commit()
                flash(success_message)
                
                if redirect_url:
                    return redirect(url_for(redirect_url))
                return func(*args, **kwargs)
                
            except Exception as e:
                db.session.rollback()
                flash(f'{error_message}: {str(e)}')
                logger.error(f"Database operation error: {e}")
                
                if redirect_url:
                    return redirect(url_for(redirect_url))
                return func(*args, **kwargs)
        return wrapper
    return decorator


def safe_database_operation(operation_func, success_msg: str, error_msg: str):
    """
    安全执行数据库操作
    
    Args:
        operation_func: 数据库操作函数
        success_msg: 成功消息
        error_msg: 错误消息
        
    Returns:
        bool: 操作是否成功
    """
    from models import db
    
    try:
        operation_func()
        db.session.commit()
        flash(success_msg)
        return True
    except Exception as e:
        db.session.rollback()
        flash(f'{error_msg}: {str(e)}')
        logger.error(f"Database operation error: {e}")
        return False


def validate_api_key_data(form_data: dict) -> tuple[bool, str]:
    """
    验证API密钥表单数据
    
    Args:
        form_data: 表单数据字典
        
    Returns:
        tuple: (是否有效, 错误消息)
    """
    provider = form_data.get('provider', '').strip()
    api_key = form_data.get('api_key', '').strip()
    
    if not provider:
        return False, "请选择AI提供商"
    
    if not api_key:
        return False, "请输入API密钥"
    
    return True, ""


def get_provider_display_name(provider: str) -> str:
    """获取提供商显示名称"""
    from config import Config
    return Config.SUPPORTED_PROVIDERS.get(provider, provider)


def format_error_response(error_msg: str, status_code: int = 400) -> tuple:
    """格式化错误响应"""
    from flask import jsonify
    return jsonify({'error': error_msg}), status_code 