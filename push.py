# push.py
import os
import time

import requests
import logging

logger = logging.getLogger(__name__)


class PushNotification:
    def __init__(self):
        self.pushplus_url = "https://www.pushplus.plus/send"
        self.telegram_base_url = "https://api.telegram.org/bot{}/sendMessage"
        self.headers = {
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
        }

        # 设置代理（如果环境变量中有的话）
        self.proxies = {}
        if os.getenv('https_proxy'):
            self.proxies['https'] = os.getenv('https_proxy')
        if os.getenv('http_proxy'):
            self.proxies['http'] = os.getenv('http_proxy')

    def push_pushplus(self, content, token, retries=3, delay=3, timeout=5):

        """
        Send notification via PushPlus with retry mechanism and timeout
        """
        for attempt in range(retries):
            try:
                params = {
                    "token": token,
                    "content": content+attempt
                }
                logger.info("PushPlus通知发送尝试 #第%d次。", attempt + 1)
                response = requests.get(self.pushplus_url, headers=self.headers, params=params, timeout=timeout)
                response.raise_for_status()
                logger.info("PushPlus Response: %s", response.text)
                return True
            except requests.exceptions.RequestException as e:
                logger.error("PushPlus通知发送失败: %s", str(e))
                if attempt < retries - 1:
                    time.sleep(delay)
                else:
                    return False


    def push_telegram(self, content, bot_token, chat_id):
        """
        Telegram通知
        """
        try:
            url = self.telegram_base_url.format(bot_token)
            params = {
                "chat_id": chat_id,
                "text": content
            }

            # 发送请求，包含代理设置
            response = requests.post(
                url,
                json=params,
                proxies=self.proxies,
                timeout=30  # 添加超时设置
            )
            response.raise_for_status()
            logger.info("Telegram Response: %s", response.text)
            return True
        except requests.exceptions.ProxyError as e:
            logger.error("Telegram代理连接失败: %s", str(e))
            # 尝试不使用代理直接连接
            try:
                response = requests.post(url, json=params, timeout=30)
                response.raise_for_status()
                logger.info("Telegram直连成功: %s", response.text)
                return True
            except Exception as e2:
                logger.error("Telegram直连也失败: %s", str(e2))
                return False
        except Exception as e:
            logger.error("Telegram通知发送失败: %s", str(e))
            return False


def push(content, method, pushplus_token=None, telegram_bot_token=None, telegram_chat_id=None):
    """
    统一推送接口
    """
    notifier = PushNotification()

    if method == "pushplus":
        if not pushplus_token:
            pushplus_token = os.getenv("PUSHPLUS_TOKEN", "a3d80d84ff434ee79b5db33fc45b6d1d")  # 替换为你的PushPlus token
        return notifier.push_pushplus(content, pushplus_token)

    elif method == "telegram":
        if not all([telegram_bot_token, telegram_chat_id]):
            telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN")  # 替换为你的Telegram bot token
            telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID")  # 替换为你的Telegram chat ID
        return notifier.push_telegram(content, telegram_bot_token, telegram_chat_id)

    else:
        raise ValueError("无效的通知渠道. 请选择 'pushplus' 或者 'telegram'")
