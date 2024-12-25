import os
import time
import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class PushNotification:
    """
    推送通知类：支持 PushPlus 和 Telegram 推送
    """

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

    def push_pushplus(self, content: str, token: str, retries: int = 6, delay: int = 300, timeout: int = 5) -> bool:

        """
        PushPlus 推送通知
        :param content: 推送内容
        :param token: PushPlus Token
        :param retries: 重试次数
        :param delay: 每次重试之间的延迟
        :param timeout: 请求超时时间
        :return: 是否推送成功
        """
        params = {"token": token, "content": content}
        for attempt in range(retries):
            try:
                logger.info("PushPlus通知发送尝试 #%d", attempt + 1)
                response = requests.get(self.pushplus_url, headers=self.headers, params=params, timeout=timeout)
                response.raise_for_status()
                logger.info("PushPlus Response: %s", response.text)
                return True
            except requests.exceptions.RequestException as e:
                logger.error("PushPlus通知发送失败: %s", e)
                if attempt < retries - 1:
                    time.sleep(delay)
        return False

    def push_telegram(self, content: str, bot_token: str, chat_id: str) -> bool:
        """
        Telegram 推送通知
        :param content: 推送内容
        :param bot_token: Telegram Bot Token
        :param chat_id: Telegram Chat ID
        :return: 是否推送成功
        """
        url = self.telegram_base_url.format(bot_token)
        params = {"chat_id": chat_id, "text": content}

        try:
            # 使用代理发送请求
            response = requests.post(url, json=params, proxies=self.proxies, timeout=30)
            response.raise_for_status()
            logger.info("Telegram通知成功: %s", response.text)
            return True
        except requests.exceptions.ProxyError as proxy_error:
            logger.warning("Telegram代理连接失败，尝试直连: %s", proxy_error)
            # 尝试直连
            try:
                response = requests.post(url, json=params, timeout=30)
                response.raise_for_status()
                logger.info("Telegram直连通知成功: %s", response.text)
                return True
            except requests.RequestException as e:
                logger.error("Telegram直连也失败: %s", e)
        except requests.RequestException as e:
            logger.error("Telegram通知发送失败: %s", e)
        return False


def push(
    content: str,
    method: str,
    pushplus_token: Optional[str] = None,
    telegram_bot_token: Optional[str] = None,
    telegram_chat_id: Optional[str] = None
) -> bool:
    """
    统一推送接口
    :param content: 推送内容
    :param method: 推送方式 ("pushplus" 或 "telegram")
    :param pushplus_token: PushPlus 的 Token（可选）
    :param telegram_bot_token: Telegram Bot 的 Token（可选）
    :param telegram_chat_id: Telegram 的 Chat ID（可选）
    :return: 是否推送成功
    """
    notifier = PushNotification()

    if method == "pushplus":
        token = pushplus_token or os.getenv("PUSHPLUS_TOKEN", "YOUR_PUSHPLUS_TOKEN")
        return notifier.push_pushplus(content, token)

    elif method == "telegram":
        bot_token = telegram_bot_token or os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN")
        chat_id = telegram_chat_id or os.getenv("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID")
        return notifier.push_telegram(content, bot_token, chat_id)

    else:
        raise ValueError("无效的通知渠道，请选择 'pushplus' 或 'telegram'")