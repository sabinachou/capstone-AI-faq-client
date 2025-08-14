#!/bin/bash

# Azure App Service 启动脚本
echo "Starting FAQ Backend Application..."

# 设置工作目录
cd /home/site/wwwroot

# 安装依赖
echo "Installing dependencies..."
pip install -r requirements.txt

# 设置环境变量
export PYTHONPATH=/home/site/wwwroot

# 初始化数据库（如果需要）
echo "Initializing database..."
python -c "
try:
    from app import app, db
    with app.app_context():
        db.create_all()
    print('Database initialized successfully')
except Exception as e:
    print(f'Database initialization error: {e}')
"

# 启动应用
echo "Starting application..."
exec gunicorn --bind 0.0.0.0:$PORT --timeout 120 --workers 2 app:app