# 使用官方的 Python 基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录内容到容器中的 /app 目录
COPY . /app

# 安装运行所需的依赖
RUN pip install certifi==2024.8.30 charset-normalizer==3.4.0 idna==3.10 requests==2.32.3 urllib3==2.2.3

# 创建 logs 目录
RUN mkdir -p /app/logs

# 添加定时任务
RUN echo "0 1 * * * /usr/local/bin/python /app/main.py >> /app/logs/$(date +\%Y-\%m-\%d).log 2>&1" > /etc/cron.d/mycron

# 给定时任务文件添加可执行权限
RUN chmod 0644 /etc/cron.d/mycron

# 应用定时任务
RUN crontab /etc/cron.d/mycron

# 启动 cron 服务并在前台运行
CMD ["cron", "-f"]
