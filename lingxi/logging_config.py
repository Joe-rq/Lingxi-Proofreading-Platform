"""
灵犀校对平台 - 日志配置模块
"""

import logging
import logging.handlers
import os
from config import Config


def setup_logging():
    """设置应用日志配置"""
    
    # 创建日志目录
    log_dir = os.path.dirname(Config.LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 设置日志级别
    log_level = getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO)
    
    # 配置根日志器
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # 控制台输出
            logging.handlers.RotatingFileHandler(
                Config.LOG_FILE,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
        ]
    )
    
    # 设置第三方库的日志级别
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    logger = logging.getLogger(__name__)
    logger.info("Logging configuration completed")
    
    return logger 