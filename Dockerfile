FROM python:3.11-slim

WORKDIR /app

# 复制项目文件
COPY requirements.txt .
COPY server.py .
COPY run.py .
COPY rootdata_api.py .
COPY .env.example .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口（注意：实际端口可能会根据可用性而变化）
EXPOSE 8400-8500

# 启动命令（使用 run.py 脚本以更可靠地处理端口冲突）
CMD ["python", "run.py"]
