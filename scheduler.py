import os
import sys
import logging
import subprocess
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

# 配置日志输出到标准输出
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

def run_job():
    logging.info("开始执行定时阅读任务...")
    try:
        # 以子进程运行 main.py，以保持运行环境的独立和纯净
        subprocess.run(
            [sys.executable, "main.py"],
            capture_output=False,
            check=True
        )
        logging.info("定时阅读任务执行成功。")
    except subprocess.CalledProcessError as e:
        logging.error(f"定时任务执行失败，退出码：{e.returncode}")
    except Exception as e:
        logging.error(f"运行任务时发生异常: {e}")

if __name__ == "__main__":
    cron_schedule = os.getenv("CRON_SCHEDULE", "0 1 * * *")
    timezone = os.getenv("TZ", "Asia/Shanghai")
    
    logging.info(f"使用时区: {timezone}")
    logging.info(f"解析定时规则 (CRON_SCHEDULE): {cron_schedule}")
    
    try:
        # 将 cron 表达式解析为 CronTrigger 参数
        # 标准 cron 格式为: 分 时 日 月 周
        fields = cron_schedule.strip().split()
        if len(fields) != 5:
            raise ValueError(f"无效的 cron 表达式，必须包含 5 个字段: {cron_schedule}")
            
        trigger = CronTrigger(
            minute=fields[0],
            hour=fields[1],
            day=fields[2],
            month=fields[3],
            day_of_week=fields[4],
            timezone=timezone
        )
        
        scheduler = BlockingScheduler()
        scheduler.add_job(run_job, trigger)
        
        # 计算下一次运行时间并记录日志
        next_run = trigger.get_next_fire_time(None, datetime.now(trigger.timezone))
        logging.info(f"调度器已启动。下一次任务执行时间: {next_run}")
        
        scheduler.start()
    except Exception as e:
        logging.critical(f"启动调度器失败: {e}")
        sys.exit(1)
