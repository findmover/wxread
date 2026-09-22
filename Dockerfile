FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 设置时区为中国时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV PATH="/usr/local/bin:${PATH}"

# 复制项目文件
COPY main.py push.py config.py log_utils.py scheduler.py ./

# 安装 Python 依赖
RUN pip install --no-cache-dir \
    requests>=2.32.3 \
    urllib3>=2.2.3 \
    apscheduler>=3.10.0

# 启动命令
CMD ["python", "scheduler.py"]
