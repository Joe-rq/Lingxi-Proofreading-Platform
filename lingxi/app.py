from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
import json
import logging
from datetime import datetime

from config import Config
from models import db, User, APIKey, ProofreadingHistory
from ai_services import get_ai_service

app = Flask(__name__)
app.config.from_object(Config)

# 初始化扩展
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = '请先登录以访问此页面'

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    """主页 - 校对界面"""
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    # 获取用户可用的AI模型
    available_models = []
    for api_key in current_user.api_keys:
        provider_name = Config.SUPPORTED_PROVIDERS.get(api_key.provider, api_key.provider)
        available_models.append({
            'provider': api_key.provider,
            'name': provider_name
        })
    
    return render_template('index.html', available_models=available_models)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            flash('用户名已存在')
            return render_template('register.html')
        
        # 创建新用户
        user = User(username=username)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('注册成功！请登录')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'注册失败: {str(e)}')
            logger.error(f"Registration error: {e}")
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('用户名或密码错误')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """用户登出"""
    logout_user()
    return redirect(url_for('login'))

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """设置页面 - API密钥管理"""
    if request.method == 'POST':
        provider = request.form['provider']
        api_key = request.form['api_key']
        base_url = request.form.get('base_url', '')
        
        # 检查是否已存在相同提供商的密钥
        existing_key = APIKey.query.filter_by(
            user_id=current_user.id,
            provider=provider
        ).first()
        
        if existing_key:
            flash(f'{Config.SUPPORTED_PROVIDERS.get(provider, provider)} 的API密钥已存在，请先删除再添加')
            return redirect(url_for('settings'))
        
        # 创建新的API密钥记录
        try:
            new_api_key = APIKey(
                user_id=current_user.id,
                provider=provider,
                base_url=base_url if provider == 'custom_openai' else None
            )
            new_api_key.set_api_key(api_key, app.config['ENCRYPTION_KEY'])
            
            db.session.add(new_api_key)
            db.session.commit()
            
            flash(f'{Config.SUPPORTED_PROVIDERS.get(provider, provider)} API密钥添加成功')
        except Exception as e:
            db.session.rollback()
            flash(f'添加API密钥失败: {str(e)}')
            logger.error(f"API key addition error: {e}")
    
    # 获取用户的API密钥列表
    user_api_keys = APIKey.query.filter_by(user_id=current_user.id).all()
    
    return render_template('settings.html', 
                         api_keys=user_api_keys,
                         supported_providers=Config.SUPPORTED_PROVIDERS)

@app.route('/delete_api_key/<int:key_id>')
@login_required
def delete_api_key(key_id):
    """删除API密钥"""
    api_key = APIKey.query.filter_by(id=key_id, user_id=current_user.id).first()
    
    if api_key:
        try:
            db.session.delete(api_key)
            db.session.commit()
            flash('API密钥删除成功')
        except Exception as e:
            db.session.rollback()
            flash(f'删除API密钥失败: {str(e)}')
            logger.error(f"API key deletion error: {e}")
    else:
        flash('API密钥不存在')
    
    return redirect(url_for('settings'))

@app.route('/api/proofread', methods=['POST'])
@login_required
def api_proofread():
    """执行文本校对的API接口"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        provider = data.get('provider', '')
        
        if not text:
            return jsonify({'error': '请输入要校对的文本'}), 400
        
        if not provider:
            return jsonify({'error': '请选择AI模型'}), 400
        
        # 查找用户的API密钥
        api_key_record = APIKey.query.filter_by(
            user_id=current_user.id,
            provider=provider
        ).first()
        
        if not api_key_record:
            return jsonify({'error': f'未找到 {provider} 的API密钥'}), 400
        
        # 解密API密钥
        api_key = api_key_record.get_api_key(app.config['ENCRYPTION_KEY'])
        
        # 获取AI服务并执行校对
        ai_service = get_ai_service(provider, api_key, api_key_record.base_url)
        result = ai_service.proofread(text)
        
        # 保存校对历史
        try:
            history = ProofreadingHistory(
                user_id=current_user.id,
                original_text=text,
                corrected_text=result.corrected_text,
                issues_found=json.dumps(result.issues, ensure_ascii=False),
                model_used=provider
            )
            db.session.add(history)
            db.session.commit()
        except Exception as e:
            logger.error(f"Failed to save proofreading history: {e}")
        
        return jsonify({
            'corrected_text': result.corrected_text,
            'issues': result.issues
        })
        
    except Exception as e:
        logger.error(f"Proofreading error: {e}")
        return jsonify({'error': f'校对失败: {str(e)}'}), 500

@app.route('/history')
@login_required
def history():
    """校对历史页面"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    histories = ProofreadingHistory.query.filter_by(user_id=current_user.id)\
                                        .order_by(ProofreadingHistory.created_at.desc())\
                                        .paginate(page=page, per_page=per_page, error_out=False)
    
    # 解析issues_found JSON
    for history in histories.items:
        try:
            history.issues = json.loads(history.issues_found) if history.issues_found else []
        except:
            history.issues = []
    
    return render_template('history.html', histories=histories)

# 错误处理
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# 创建数据库表
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True) 