# 灵犀文档校对平台 - 使用示例

## AI模型管理功能使用示例

### 1. 基础配置示例

#### 添加API密钥并选择模型
```bash
# 1. 访问设置页面
# 2. 选择AI服务商（例如：DeepSeek）
# 3. 输入API密钥
# 4. 选择要启用的模型：
#    - DeepSeek-R1（推理增强模型）
#    - DeepSeek-V3（中文优化模型）
# 5. 保存配置
```

#### 主页使用模型
```bash
# 在主页的模型选择下拉菜单中会显示：
# - "DeepSeek - DeepSeek-R1"
# - "DeepSeek - DeepSeek-V3" 
# 选择其中一个进行文本校对
```

### 2. 自定义模型管理示例

#### 为OpenAI添加自定义模型
```javascript
// 通过API添加自定义模型
fetch('/api/models/add', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    provider: 'openai',
    model_id: 'gpt-4o-turbo-custom',
    model_name: 'GPT-4o Turbo 自定义版',
    description: '针对文档校对优化的GPT-4o Turbo模型'
  })
})
```

#### 为DeepSeek添加实验性模型
```javascript
// 添加DeepSeek实验模型
fetch('/api/models/add', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    provider: 'deepseek',
    model_id: 'deepseek-r2-preview',
    model_name: 'DeepSeek-R2 预览版',
    description: 'DeepSeek第二代推理模型预览版，实验性功能'
  })
})
```

#### 更新现有模型信息
```javascript
// 更新模型描述
fetch('/api/models/update', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    provider: 'qwen',
    model_id: 'qwen3-235b',
    model_name: 'Qwen3-235B 企业版',
    description: '2350亿参数的Qwen3模型，企业级优化版本'
  })
})
```

### 3. 不同场景的模型选择建议

#### 中文文档校对推荐
```yaml
首选模型:
  - "DeepSeek - DeepSeek-R1": 强化学习优化，中文理解卓越
  - "智谱AI - GLM-4-Flash": 中文专用优化，响应快速
  - "Qwen - Qwen3-235B": 超大参数，中文能力强

备选模型:
  - "DeepSeek - DeepSeek-V3": 大上下文，适合长文档
  - "智谱AI - GLM-4-Long": 超长文本处理能力
```

#### 英文文档校对推荐
```yaml
首选模型:
  - "OpenAI - GPT-4o": 多模态，推理能力强
  - "OpenAI - o3": 顶级推理能力
  - "Google - Gemini 2.5 Pro": 多语言支持

备选模型:
  - "OpenAI - GPT-4 Turbo": 大上下文处理
  - "Google - Gemini 1.5 Pro": 高性能模型
```

#### 代码文档校对推荐
```yaml
首选模型:
  - "DeepSeek - DeepSeek Coder": 代码专用优化
  - "OpenAI - GPT-4o": 多模态理解代码
  
备选模型:
  - "OpenAI - GPT-4": 强大的逻辑推理
  - "DeepSeek - DeepSeek-R1": 推理增强适合技术文档
```

### 4. API使用示例

#### 获取用户可用模型
```javascript
// 获取当前用户配置的所有可用模型
fetch('/api/user/models')
  .then(response => response.json())
  .then(data => {
    console.log('可用模型:', data.models);
    // 输出示例:
    // [
    //   {
    //     "provider": "deepseek",
    //     "provider_name": "DeepSeek",
    //     "model_id": "deepseek-r1",
    //     "model_name": "DeepSeek-R1",
    //     "description": "最新推理增强模型，强化学习优化",
    //     "full_name": "DeepSeek - DeepSeek-R1"
    //   }
    // ]
  });
```

#### 执行文档校对
```javascript
// 使用指定模型进行校对
fetch('/api/proofread', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: '需要校对的文本内容',
    provider: 'deepseek',
    model: 'deepseek-r1'
  })
})
.then(response => response.json())
.then(data => {
  console.log('校对结果:', data.corrected_text);
  console.log('发现的问题:', data.issues);
});
```

### 5. 前端界面操作示例

#### 设置页面操作流程
```bash
1. 登录系统
2. 点击导航栏的"设置"
3. 在"API密钥管理"标签页：
   - 选择AI服务商
   - 输入API密钥
   - 选择要启用的模型
   - 保存配置

4. 切换到"自定义模型"标签页：
   - 添加自定义模型配置
   - 编辑现有模型信息
   - 按提供商筛选查看
```

#### 主页校对操作流程
```bash
1. 访问主页
2. 在"选择AI模型"下拉菜单中选择具体模型
   例如："DeepSeek - DeepSeek-R1"
3. 在文本框中输入要校对的内容
4. 点击"开始校对"按钮
5. 等待处理完成
6. 查看校对结果和问题分析
7. 可以复制结果或下载为文件
```

### 6. 高级配置示例

#### 为不同团队配置不同模型
```yaml
# 技术文档团队
技术团队配置:
  - DeepSeek Coder (代码文档)
  - GPT-4o (技术规范)
  - DeepSeek-R1 (架构设计)

# 市场营销团队  
营销团队配置:
  - GLM-4-Flash (中文营销文案)
  - GPT-4o (英文内容)
  - Gemini 2.5 Pro (多语言支持)

# 学术研究团队
研究团队配置:
  - GPT-4 Turbo (长篇论文)
  - DeepSeek-V3 (中文学术)
  - Qwen3-235B (复杂分析)
```

#### 成本优化配置
```yaml
# 成本敏感场景
经济配置:
  首选: GLM-3 Turbo (经济实用)
  备选: GPT-3.5 Turbo (成本控制)
  
# 高质量场景
高级配置:
  首选: GPT-4o (顶级质量)
  备选: DeepSeek-R1 (推理增强)
  备选: Qwen3-235B (超大参数)
```

### 7. 故障排除示例

#### 常见问题处理
```bash
# 问题1: 模型不可用
解决方案:
1. 检查API密钥是否有效
2. 确认模型在"模型配置"中已启用
3. 验证提供商服务状态

# 问题2: 校对质量不理想
解决方案:
1. 尝试更换为更强大的模型
2. 检查文本长度是否超出模型限制
3. 考虑使用专用模型（如代码用DeepSeek Coder）

# 问题3: 响应速度慢
解决方案:
1. 选择"Flash"或"Turbo"类型的快速模型
2. 分段处理长文档
3. 使用轻量级模型进行初步校对
```

### 8. 最佳实践建议

#### 模型选择原则
```yaml
文档类型匹配:
  - 中文文档 → DeepSeek/智谱AI模型
  - 英文文档 → OpenAI/Google模型  
  - 代码文档 → DeepSeek Coder
  - 长文档 → 支持大上下文的模型

质量要求匹配:
  - 高质量要求 → 使用顶级模型 (GPT-4o, o3, DeepSeek-R1)
  - 快速处理 → 使用快速模型 (Flash, Turbo系列)
  - 成本控制 → 使用经济模型 (3.5 Turbo, GLM-3 Turbo)
```

#### 配置管理建议
```yaml
定期维护:
  - 每月更新模型配置
  - 关注新模型发布
  - 清理不用的自定义模型

团队协作:
  - 统一团队模型配置标准
  - 分享有效的自定义模型配置
  - 建立模型使用指南

性能监控:
  - 记录不同模型的校对效果
  - 监控API使用成本
  - 优化模型选择策略
```

这些示例展示了如何充分利用灵犀文档校对平台的AI模型管理功能，实现高效、灵活的文档校对工作流程。 