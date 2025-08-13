# AI FAQ Assistant - 用户指南

## 项目概述

AI FAQ Assistant 是一个智能问答系统，结合了传统FAQ管理和AI智能回答功能。系统支持连续对话、情感识别、关键词提取和用户反馈等高级功能。

### 主要功能
- 智能FAQ问答系统
- 连续对话会话管理
- 情感识别和人工转接
- 关键词提取和分类
- 用户认证和权限管理
- 管理员仪表板和数据分析
- 用户反馈和满意度评价

## 技术栈

### 前端 (React)
- **框架**: React 19.1.0
- **路由**: React Router DOM 7.6.3
- **HTTP客户端**: Axios 1.11.0
- **图表库**: Chart.js 4.5.0 + React-ChartJS-2 5.3.0
- **构建工具**: Create React App

### 后端 (Flask)
- **框架**: Flask 2.3.3
- **数据库ORM**: Flask-SQLAlchemy 3.0.5
- **跨域支持**: Flask-CORS 4.0.0
- **AI服务**: OpenAI 0.28.1
- **机器学习**: Scikit-learn 1.3.0
- **数据处理**: Pandas 2.0.3, NumPy 1.24.3

## 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 1. 克隆项目
```bash
git clone <repository-url>
cd AI-faq-client
```

### 2. 后端设置

#### 安装依赖
```bash
cd faq-backend
pip install -r requirements.txt
```

#### 环境配置
1. 复制环境变量文件：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，配置以下变量：
```
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///faq.db
SECRET_KEY=your_secret_key_here
```

#### 启动后端服务
```bash
python app.py
```
后端服务将在 `http://localhost:5000` 启动

### 3. 前端设置

#### 安装依赖
```bash
cd faq-frontend
npm install
```

#### 启动前端服务
```bash
npm start
```
前端应用将在 `http://localhost:3000` 启动

## 测试指南

### 后端测试

后端包含多个测试文件，位于 `faq-backend/` 目录：

#### 1. API测试
```bash
cd faq-backend
python test_api.py
```

#### 2. AI服务测试
```bash
python test_ai_service.py
```

#### 3. 关键词服务测试
```bash
python test_keyword_service.py
```

#### 4. 情感识别测试
```bash
python test_emotion_recognition.py
```

#### 5. 会话管理测试
```bash
python test_session_integration.py
```

### 前端测试
```bash
cd faq-frontend
npm test
```

### 手动测试流程

1. **用户注册/登录测试**
   - 访问 `http://localhost:3000`
   - 测试用户注册功能
   - 测试登录/登出功能

2. **FAQ问答测试**
   - 在聊天界面输入问题
   - 验证AI回答质量
   - 测试情感识别功能

3. **会话管理测试**
   - 开始连续对话会话
   - 进行多轮问答
   - 结束会话并提交反馈

4. **管理员功能测试**
   - 使用管理员账户登录
   - 测试FAQ增删改查
   - 查看数据分析仪表板

## 代码架构

### 前端架构

```
faq-frontend/src/
├── App.js                 # 主应用组件，路由配置
├── index.js              # 应用入口点
├── style.css             # 全局样式
├── api/                  # API调用层
│   ├── authApi.js        # 认证相关API
│   └── faqApi.js         # FAQ相关API
├── components/           # 可复用组件
│   ├── chartdashboard.js # 图表仪表板组件
│   ├── chatinput.js      # 聊天输入组件
│   └── messagebubble.js  # 消息气泡组件
└── pages/                # 页面组件
    ├── adminpage.js      # 管理员页面
    ├── chatpage.js       # 聊天页面
    └── loginpage.js      # 登录页面
```

#### 主要组件说明

- **App.js**: 应用主组件，处理路由和全局状态管理
- **ChatPage**: 用户聊天界面，包含会话管理和消息显示
- **AdminPage**: 管理员界面，包含FAQ管理和数据分析
- **LoginPage**: 用户认证界面，支持登录和注册
- **MessageBubble**: 消息显示组件，支持情感识别显示
- **ChartDashboard**: 数据可视化组件，显示使用统计

### 后端架构

```
faq-backend/
├── app.py                    # Flask应用主文件，API路由
├── config.py                 # 配置文件
├── models.py                 # 数据库模型定义
├── ai_service.py             # AI服务模块
├── keyword_service.py        # 关键词提取服务
├── conversation_service.py   # 会话管理服务
└── test_*.py                # 各种测试文件
```

#### 核心模块说明

1. **app.py**: Flask应用主文件
   - 定义所有API端点
   - 处理HTTP请求和响应
   - 集成各个服务模块

2. **models.py**: 数据库模型
   - `FAQ`: FAQ条目模型
   - `User`: 用户模型
   - `Log`: 问题日志模型
   - `ConversationSession`: 会话模型
   - `Feedback`: 用户反馈模型

3. **ai_service.py**: AI智能服务
   - OpenAI API集成
   - 语义相似度计算
   - 情感识别
   - 智能回答生成

4. **keyword_service.py**: 关键词处理
   - 关键词提取
   - 问题分类
   - 文本预处理

5. **conversation_service.py**: 会话管理
   - 会话创建和结束
   - 会话状态管理
   - 反馈处理

### API接口文档

详细的API文档请参考 `faq-backend/API_list.md` 文件。

主要API端点：
- `GET /api/faqs` - 获取所有FAQ
- `POST /api/faqs` - 创建新FAQ
- `POST /api/chat` - 智能问答
- `POST /api/session/start` - 开始会话
- `POST /api/session/end` - 结束会话
- `POST /api/login` - 用户登录
- `POST /api/register` - 用户注册

## 数据库说明

### 数据库文件位置
- 主数据库: `faq-backend/faq.db`
- 备份数据库: `instance/faq.db`

### 数据库表结构

#### 1. faqs 表
```sql
CREATE TABLE faqs (
    id INTEGER PRIMARY KEY,
    question VARCHAR(255) NOT NULL,
    answer VARCHAR(255) NOT NULL
);
```

#### 2. users 表
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'employee',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### 3. log 表
```sql
CREATE TABLE log (
    id INTEGER PRIMARY KEY,
    question VARCHAR(255) NOT NULL,
    keywords VARCHAR(255),
    category VARCHAR(100),
    session_id VARCHAR(255),
    is_session_end BOOLEAN DEFAULT FALSE,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### 4. conversation_sessions 表
```sql
CREATE TABLE conversation_sessions (
    id INTEGER PRIMARY KEY,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    user_id INTEGER,
    start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    end_time DATETIME,
    is_active BOOLEAN DEFAULT TRUE,
    question_count INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

#### 5. feedback 表
```sql
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY,
    satisfied BOOLEAN NOT NULL,
    session_id VARCHAR(255),
    rating INTEGER,
    comment TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 查看数据库数据

#### 如果下载了SQLite explorer，可以在上面> open database> 选择faq-backend/faq.db

#### 使用SQLite命令行工具
```bash
# 进入数据库
sqlite3 faq-backend/faq.db

# 查看所有表
.tables

# 查看表结构
.schema faqs

# 查询数据
SELECT * FROM faqs;
SELECT * FROM users;
SELECT * FROM log ORDER BY timestamp DESC LIMIT 10;

# 退出
.quit
```

#### 使用Python脚本查看
```python
import sqlite3

# 连接数据库
conn = sqlite3.connect('faq-backend/faq.db')
cursor = conn.cursor()

# 查询FAQ数据
cursor.execute('SELECT * FROM faqs')
faqs = cursor.fetchall()
print('FAQs:', faqs)

# 查询用户数据
cursor.execute('SELECT id, username, email, role FROM users')
users = cursor.fetchall()
print('Users:', users)

# 查询最近的问题日志
cursor.execute('SELECT * FROM log ORDER BY timestamp DESC LIMIT 5')
logs = cursor.fetchall()
print('Recent logs:', logs)

conn.close()
```

## 常见问题和故障排除

### 1. 后端启动失败
- 检查Python版本和依赖安装
- 确认 `.env` 文件配置正确
- 检查端口5000是否被占用

### 2. 前端启动失败
- 检查Node.js版本
- 删除 `node_modules` 重新安装: `rm -rf node_modules && npm install`
- 检查端口3000是否被占用

### 3. AI功能不工作
- 检查OpenAI API密钥配置
- 确认网络连接正常
- 查看后端日志错误信息

### 4. 数据库问题
- 删除现有数据库文件重新初始化
- 检查数据库文件权限
- 查看SQLAlchemy错误日志

### 5. 跨域问题
- 确认Flask-CORS配置正确
- 检查前端API请求URL
- 验证 `withCredentials` 设置

## 开发指南

### 添加新功能

1. **后端API开发**
   - 在 `app.py` 中添加新的路由
   - 在 `models.py` 中定义新的数据模型
   - 编写相应的测试文件

2. **前端组件开发**
   - 在 `components/` 或 `pages/` 中创建新组件
   - 在 `api/` 中添加API调用函数
   - 更新路由配置

