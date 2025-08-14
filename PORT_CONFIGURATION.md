# 端口配置说明

## 概述
本项目已统一所有端口配置为 **5000**，避免端口不一致的问题。

## 端口配置详情

### 后端 (Flask)
- **端口**: 5000
- **配置文件**: `faq-backend/app.py`
- **默认端口**: 从8000改为5000
- **CORS配置**: 允许来自 `http://localhost:5000` 的请求

### 前端 (React)
- **端口**: 5000 (覆盖默认的3000端口)
- **配置文件**: `faq-frontend/src/config.js`
- **API基础URL**: `http://127.0.0.1:5000`

## 启动方式

### 方式1: 使用启动脚本 (推荐)

#### macOS/Linux
```bash
./start.sh
```

#### Windows
```cmd
start.bat
```

### 方式2: 手动启动

#### 启动后端
```bash
cd faq-backend
python app.py
```

#### 启动前端
```bash
cd faq-frontend
PORT=5000 npm start
```

## 访问地址

- **前端应用**: http://localhost:5000
- **后端API**: http://localhost:5000/api
- **健康检查**: http://localhost:5000/api/health

## 配置文件

### 后端配置 (`faq-backend/app.py`)
```python
port = int(os.environ.get('PORT', 5000))  # 默认端口5000
CORS(app, resources={r"/*": {"origins": "http://localhost:5000"}})
```

### 前端配置 (`faq-frontend/src/config.js`)
```javascript
export const API_CONFIG = {
  BACKEND_URL: 'http://127.0.0.1:5000',
  API_BASE: 'http://127.0.0.1:5000/api',
  FRONTEND_PORT: 5000,
  BACKEND_PORT: 5000
};
```

## 环境变量

如果需要自定义端口，可以设置环境变量：

```bash
# 后端端口
export PORT=5000

# 前端端口
export PORT=5000
```

## 故障排除

### 端口被占用
如果5000端口被占用，可以修改配置文件中的端口号，或者使用环境变量：

```bash
PORT=5001 ./start.sh
```

### 检查端口状态
```bash
# 检查5000端口是否被占用
lsof -i :5000

# 或者使用netstat
netstat -an | grep 5000
```

## 注意事项

1. 确保前后端端口配置一致
2. 修改端口后需要重启服务
3. 生产环境建议使用环境变量配置端口
4. CORS配置需要与前端端口匹配


