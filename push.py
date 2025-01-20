# push.py 支持 PushPlus 、wxpusher、Telegram 的消息推送模块
import os
import random
import time
import json
import requests
import logging
from config import PUSHPLUS_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_BOT_TOKEN, WXPUSHER_SPT

logger = logging.getLogger(__name__)


class PushNotification:
    def __init__(self):
        self.pushplus_url = "https://www.pushplus.plus/send"
        self.telegram_url = "https://api.telegram.org/bot{}/sendMessage"
        self.headers = {'Content-Type': 'application/json'}
        # 从环境变量获取代理设置
        self.proxies = {
            'http': os.getenv('http_proxy'),
            'https': os.getenv('https_proxy')
        }
        self.wxpusher_simple_url = "https://wxpusher.zjiecode.com/api/send/message/{}/{}"

    def push_pushplus(self, content, token):
        """PushPlus消息推送"""
        attempts = 5
        for attempt in range(attempts):
            try:
                response = requests.post(
                    self.pushplus_url,
                    data=json.dumps({
                        "token": token,
                        "title": "微信阅读推送...",
                        "content": content
                    }).encode('utf-8'),
                    headers=self.headers,
                    timeout=10
                )
                response.raise_for_status()
                logger.info("✅ PushPlus响应: %s", response.text)
                break  # 成功推送，跳出循环
            except requests.exceptions.RequestException as e:
                logger.error("❌ PushPlus推送失败: %s", e)
                if attempt < attempts - 1:  # 如果不是最后一次尝试
                    sleep_time = random.randint(180, 360)  # 随机3到6分钟
                    logger.info("将在 %d 秒后重试...", sleep_time)
                    time.sleep(sleep_time)

    def push_telegram(self, content, bot_token, chat_id):
        """Telegram消息推送，失败时自动尝试直连"""
        url = self.telegram_url.format(bot_token)
        payload = {"chat_id": chat_id, "text": content}

        try:
            # 先尝试代理
            response = requests.post(url, json=payload, proxies=self.proxies, timeout=30)
            logger.info("✅ Telegram响应: %s", response.text)
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error("❌ Telegram代理发送失败: %s", e)
            try:
                # 代理失败后直连
                response = requests.post(url, json=payload, timeout=30)
                response.raise_for_status()
                return True
            except Exception as e:
                logger.error("❌ Telegram发送失败: %s", e)
                return False
    
    def push_wxpusher(self, content, spt):
        """WxPusher消息推送（极简方式）"""
        attempts = 5
        url = self.wxpusher_simple_url.format(spt, content)
        
        for attempt in range(attempts):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                logger.info("✅ WxPusher响应: %s", response.text)
                break
            except requests.exceptions.RequestException as e:
                logger.error("❌ WxPusher推送失败: %s", e)
                if attempt < attempts - 1:
                    sleep_time = random.randint(180, 360)
                    logger.info("将在 %d 秒后重试...", sleep_time)
                    time.sleep(sleep_time)


"""外部调用"""


def push(content, method):
    """统一推送接口，支持 PushPlus、Telegram 和 WxPusher"""
    notifier = PushNotification()

    if method == "pushplus":
        token = PUSHPLUS_TOKEN
        return notifier.push_pushplus(content, token)
    elif method == "telegram":
        bot_token = TELEGRAM_BOT_TOKEN
        chat_id = TELEGRAM_CHAT_ID
        return notifier.push_telegram(content, bot_token, chat_id)
    elif method == "wxpusher":
        return notifier.push_wxpusher(content, WXPUSHER_SPT)
    else:
        raise ValueError("❌ 无效的通知渠道，请选择 'pushplus'、'telegram' 或 'wxpusher'")
