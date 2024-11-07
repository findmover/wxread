# push.py
import os
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PushNotification:
    def __init__(self):
        self.pushplus_url = "https://www.pushplus.plus/send"
        self.telegram_base_url = "https://api.telegram.org/bot{}/sendMessage"
        self.headers = {
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
        }

    def push_pushplus(self, content, token):
        """
        Send notification via PushPlus
        """
        try:
            params = {
                "token": token,
                "content": content
            }
            response = requests.get(self.pushplus_url, headers=self.headers, params=params)
            response.raise_for_status()
            logger.info("PushPlus Response: %s", response.text)
            return True
        except Exception as e:
            logger.error("PushPlus通知发送失败: %s", str(e))
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
            response = requests.post(url, json=params)
            response.raise_for_status()
            logger.info("Telegram Response: %s", response.text)
            return True
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
            pushplus_token = os.getenv("PUSHPLUS_TOKEN", "YOUR_PUSHPLUS_TOKEN")   # 替换为你的PushPlus token
        return notifier.push_pushplus(content, pushplus_token)
    
    elif method == "telegram":
        if not all([telegram_bot_token, telegram_chat_id]):
            telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN")  # 替换为你的Telegram bot token
            telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID")  # 替换为你的Telegram chat ID
        return notifier.push_telegram(content, telegram_bot_token, telegram_chat_id)
    
    else:
        raise ValueError("无效的通知渠道. 请选择 'pushplus' 或者 'telegram'")
