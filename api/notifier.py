import json
import os
import random
import time
from typing import Callable, Literal

import requests
from loguru import logger


class PushPlusNotifier:
    def __init__(self, token):
        self.pushplus_url = "https://www.pushplus.plus/send"
        self.token = token

    def push(
        self,
        content,
        attempt_times: int = 5,
        onSuccess: Callable = logger.success,
        onDebug: Callable = logger.debug,
        onFail: Callable = logger.error,
    ):
        """PushPlus消息推送"""
        headers = {"Content-Type": "application/json"}
        for attempt in range(attempt_times):
            try:
                response = requests.post(
                    self.pushplus_url,
                    data=json.dumps(
                        {
                            "token": self.token,
                            "title": "微信阅读推送...",
                            "content": content,
                        }
                    ).encode("utf-8"),
                    headers=headers,
                    timeout=10,
                )
                response.raise_for_status()
                onSuccess(f"✅ PushPlus响应: {response.text}")
                break
            except requests.exceptions.RequestException as e:
                onFail(f"❌ PushPlus推送失败: {e}")
                if attempt < attempt_times - 1:
                    sleep_time = random.randint(180, 360)
                    onDebug(f"将在 {sleep_time} 秒后重试...")
                    time.sleep(sleep_time)


class TelegramNotifier:
    def __init__(self, bot_token, chat_id):
        self.telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        self.chat_id = chat_id
        self.proxies = {
            "http": os.getenv("http_proxy"),
            "https": os.getenv("https_proxy"),
        }

    def push(
        self,
        content,
        onSuccess: Callable = logger.success,
        onFail: Callable = logger.error,
    ):
        """Telegram消息推送，失败时自动尝试直连"""
        payload = {"chat_id": self.chat_id, "text": content}

        try:
            # 先尝试代理
            response = requests.post(
                self.telegram_url, json=payload, proxies=self.proxies, timeout=30
            )
            response.raise_for_status()
            onSuccess(f"✅ Telegram响应: {response.text}")
            return True
        except Exception as e:
            onFail(f"❌ Telegram代理发送失败: {e}")
            try:
                # 代理失败后直连
                response = requests.post(self.telegram_url, json=payload, timeout=30)
                response.raise_for_status()
                return True
            except Exception as e:
                onFail(f"❌ Telegram发送失败: {e}")
                return False


class WxPusherNotifier:
    def __init__(self, spt):
        self.wxpusher_simple_url = (
            "https://wxpusher.zjiecode.com/api/send/message/{}/{}"
        )
        self.spt = spt

    def push(
        self,
        content,
        attempt_times: int = 5,
        onSuccess: Callable = logger.success,
        onDebug: Callable = logger.debug,
        onFail: Callable = logger.error,
    ):
        """WxPusher消息推送（极简方式）"""
        url = self.wxpusher_simple_url.format(self.spt, content)

        for attempt in range(attempt_times):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                onSuccess(f"✅ WxPusher响应: {response.json()['msg']}")
                break
            except requests.exceptions.RequestException as e:
                onFail(f"❌ WxPusher推送失败: {e}")
                if attempt < attempt_times - 1:
                    sleep_time = random.randint(180, 360)
                    onDebug(f"将在 {sleep_time} 秒后重试...")
                    time.sleep(sleep_time)


class Notifier:
    def __init__(self, method: Literal["pushplus", "telegram", "wxpusher"], config):
        if method == "pushplus":
            self.notifier = PushPlusNotifier(config["PUSHPLUS_TOKEN"])
        elif method == "telegram":
            self.notifier = TelegramNotifier(
                config["TELEGRAM_BOT_TOKEN"], config["TELEGRAM_CHAT_ID"]
            )
        elif method == "wxpusher":
            self.notifier = WxPusherNotifier(config["WXPUSHER_SPT"])
        else:
            raise ValueError(
                "❌ 无效的通知渠道，请选择 'pushplus'、'telegram' 或 'wxpusher'"
            )

    def push(self, content):
        """统一推送接口，支持 PushPlus、Telegram 和 WxPusher"""
        return self.notifier.push(content)

    def onStart(self, msg):
        logger.info(msg)
        self.push(msg)

    def onSuccess(self, msg):
        logger.success(msg)
        self.push(msg)

    def onFail(self, msg):
        logger.error(msg)
        self.push(msg)

    def onDebug(self, msg):
        logger.debug(msg)
        self.push(msg)

    def onWarning(self, msg):
        logger.warning(msg)
        self.push(msg)

    def onFinish(self, msg):
        logger.info(msg)
        self.push(msg)
