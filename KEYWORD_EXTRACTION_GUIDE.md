# 关键词提取和问题分类功能指南

## 功能概述

本系统实现了智能的关键词提取和问题分类功能，能够将用户的相似问题归纳到同一类别中，从而提供更准确的统计分析和问题管理。

### 主要特性

- **智能关键词提取**: 从用户问题中自动提取关键词
- **问题自动分类**: 将相似问题归类到预定义的类别中
- **分类统计**: 按类别统计问题频次，而不是按原始问题文本
- **详细分析**: 提供每个分类下的具体问题和关键词信息

## 功能演示

### 示例1：休假相关问题归类

**输入问题**:
- "How do I apply for vacation leave?"
- "how can i leave"
- "I need time off"

**系统处理**:
- 提取关键词: ["vacation", "leave", "time", "off"]
- 统一分类: `vacation leave`
- 统计结果: 显示为 "vacation leave: 3 次" 而不是3个独立问题

### 示例2：密码重置问题归类

**输入问题**:
- "I forgot my password"
- "How to reset my password?"
- "Password reset help"

**系统处理**:
- 提取关键词: ["password", "reset", "forgot"]
- 统一分类: `password reset`
- 统计结果: 显示为 "password reset: 3 次"

## 技术实现

### 1. 数据库模型更新

在 `models.py` 中的 `Log` 表添加了新字段：

```python
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    keywords = db.Column(db.String(255), nullable=True)  # 存储提取的关键词
    category = db.Column(db.String(100), nullable=True)  # 存储问题分类
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
```

### 2. 关键词提取服务

创建了 `keyword_service.py` 文件，包含：

#### KeywordService 类

- **extract_keywords()**: 从问题中提取关键词
- **categorize_question()**: 对问题进行分类
- **process_question()**: 综合处理问题，返回关键词和分类
- **get_category_stats()**: 获取分类统计信息

#### 预定义分类

系统支持以下问题分类：

1. **vacation leave** - 休假相关
2. **password reset** - 密码重置
3. **payroll** - 薪资相关
4. **working hours** - 工作时间
5. **vpn access** - VPN访问
6. **meeting room** - 会议室预订
7. **expense reimbursement** - 费用报销
8. **training** - 培训相关
9. **it support** - IT支持
10. **hr general** - HR一般事务

### 3. API端点更新

#### 修改的端点

**`/api/chat` (POST)**
- 在记录用户问题时自动提取关键词和分类
- 存储到数据库的 `keywords` 和 `category` 字段

**`/api/top-questions` (GET)**
- 改为按分类统计，而不是按原始问题文本
- 返回格式: `[{"question": "category_name", "count": number}]`

#### 新增端点

**`/api/categories` (GET)**
- 获取所有分类及其问题数量
- 返回格式: `[{"category": "category_name", "count": number}]`

**`/api/category-details/<category>` (GET)**
- 获取指定分类下的具体问题
- 返回格式: `[{"question": "text", "keywords": "keywords", "timestamp": "iso_date"}]`

## 使用方法

### 1. 前端集成

前端可以通过以下API获取分类统计信息：

```javascript
// 获取热门问题分类
fetch('/api/top-questions')
  .then(response => response.json())
  .then(data => {
    // data: [{"question": "vacation leave", "count": 5}, ...]
  });

// 获取所有分类
fetch('/api/categories')
  .then(response => response.json())
  .then(data => {
    // data: [{"category": "vacation leave", "count": 5}, ...]
  });

// 获取分类详情
fetch('/api/category-details/vacation%20leave')
  .then(response => response.json())
  .then(data => {
    // data: [{"question": "How do I apply for vacation leave?", "keywords": "how, apply, vacation, leave", "timestamp": "2024-01-01T10:00:00"}, ...]
  });
```

### 2. 管理界面建议

可以在管理界面中添加以下功能：

1. **分类统计图表**: 显示各类别的问题分布
2. **分类详情页面**: 点击分类查看具体问题
3. **关键词云**: 显示热门关键词
4. **趋势分析**: 显示各分类的时间趋势

## 配置和自定义

### 1. 添加新分类

在 `keyword_service.py` 的 `category_keywords` 字典中添加新分类：

```python
'new_category': {
    'keywords': ['keyword1', 'keyword2', 'phrase with spaces'],
    'patterns': [r'\b(regex_pattern)\b'],
    'category_name': 'display name'
}
```

### 2. 调整分类算法

可以修改 `categorize_question()` 方法中的评分逻辑：

- 调整关键词匹配权重
- 修改正则表达式模式权重
- 添加新的匹配规则

### 3. 停用词管理

在 `stop_words` 集合中添加或删除停用词，以改善关键词提取效果。

## 测试和验证

### 1. 单元测试

运行关键词服务测试：

```bash
python test_keyword_service.py
```

### 2. 集成测试

运行完整的API集成测试：

```bash
python test_keyword_integration.py
```

### 3. 测试用例

测试脚本包含以下测试场景：

- 关键词提取准确性
- 相似问题分类一致性
- 分类统计正确性
- 边界情况处理
- API端点功能验证

## 性能优化建议

### 1. 缓存机制

- 缓存常见问题的分类结果
- 使用Redis缓存热门分类统计

### 2. 批量处理

- 对历史数据进行批量分类处理
- 定期更新分类统计缓存

### 3. 算法优化

- 使用更高级的NLP库（如spaCy、NLTK）
- 实现机器学习分类模型
- 添加用户反馈学习机制

## 监控和维护

### 1. 分类质量监控

- 定期检查分类准确性
- 监控未分类问题（category为general的问题）
- 收集用户对分类结果的反馈

### 2. 数据分析

- 分析分类分布是否合理
- 识别需要新增的分类
- 优化现有分类的关键词和模式

### 3. 系统维护

- 定期清理过期日志数据
- 备份分类配置
- 更新关键词词典

## 故障排除

### 常见问题

1. **数据库字段不存在错误**
   - 删除现有数据库文件
   - 重启应用让Flask重新创建表结构

2. **分类结果不准确**
   - 检查关键词配置
   - 调整分类算法参数
   - 添加更多训练数据

3. **API返回500错误**
   - 检查后端日志
   - 验证数据库连接
   - 确认所有依赖已安装

## 未来扩展

### 1. 机器学习集成

- 使用预训练的语言模型
- 实现自动分类模型训练
- 添加情感分析功能

### 2. 多语言支持

- 支持中文问题分类
- 添加多语言关键词词典
- 实现跨语言问题匹配

### 3. 高级分析

- 问题相似度计算
- 自动FAQ建议
- 问题趋势预测

---

**注意**: 此功能需要重新创建数据库表结构。如果在现有系统上部署，请先备份数据，然后删除数据库文件让系统重新创建表结构。