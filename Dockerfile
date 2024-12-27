# 使用官方Python镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制requirements.txt并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制所有Python文件到容器中
COPY main.py .
COPY convert.py .
COPY push.py .

# 设置环境变量
ENV CURL_BASH=${CURL_BASH}

# 设置入口点为main.py
CMD ["python", "main.py"]