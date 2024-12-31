FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 设置时区为中国时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 安装 cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY . .

# 创建日志目录
RUN mkdir -p /app/logs

# 安装 Python 依赖
RUN pip install --no-cache-dir \
    certifi==2024.8.30 \
    charset-normalizer==3.4.0 \
    idna==3.10 \
    requests==2.32.3 \
    urllib3==2.2.3

# 创建 cron 任务
RUN echo "0 1 * * * cd /app && python main.py >> /app/logs/\$(date +\%Y-\%m-\%d).log 2>&1" > /etc/cron.d/wxread-cron
RUN chmod 0644 /etc/cron.d/wxread-cron
RUN crontab /etc/cron.d/wxread-cron

# 创建启动脚本
RUN echo '#!/bin/sh\n\
touch /app/logs/$(date +\%Y-\%m-\%d).log\n\
service cron start\n\
tail -f /app/logs/$(date +\%Y-\%m-\%d).log' > /app/start.sh
RUN chmod +x /app/start.sh

# 启动命令
CMD ["/app/start.sh"]
