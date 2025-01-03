FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 设置时区为中国时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 安装 cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*
ENV PATH="/usr/local/bin:${PATH}"

# 复制项目文件
COPY main.py push.py config.py ./

# 创建日志目录并设置权限
RUN mkdir -p /app/logs && chmod 777 /app/logs

# 安装 Python 依赖
RUN pip install --no-cache-dir \
    requests>=2.32.3 \
    urllib3>=2.2.3

# 创建 cron 任务（每天凌晨1点执行）
RUN echo "0 1 * * * cd /app && /usr/local/bin/python3 main.py >> /app/logs/\$(date +\%Y-\%m-\%d).log 2>&1" > /etc/cron.d/wxread-cron
RUN chmod 0644 /etc/cron.d/wxread-cron
RUN crontab /etc/cron.d/wxread-cron

# 启动命令
CMD ["sh", "-c", "service cron start && tail -f /dev/null"]
