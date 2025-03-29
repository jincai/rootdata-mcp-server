FROM python:3.11-slim

WORKDIR /app

# 复制项目文件
COPY requirements.txt .
COPY server.py .
COPY rootdata_api.py .
COPY .env.example .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 8400

# 启动命令
CMD ["python", "server.py"]
