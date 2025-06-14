#!/usr/bin/env python3
"""
灵犀校对平台 - 数据库初始化脚本
"""

import os
import sys

# 添加 lingxi 模块到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lingxi'))

try:
    from lingxi.app import app, db
    
    with app.app_context():
        # 创建所有数据库表
        db.create_all()
        print('✓ 数据库初始化完成')
        
except Exception as e:
    print(f'❌ 数据库初始化失败: {e}')
    sys.exit(1) 