import logging

import requests
from apprise.decorators import notify

logger = logging.getLogger(__name__)


@notify(on='pushplus', name='pushplus')
def notify_pushplus(body: str, title: str, notify_type: str, meta: dict, *args, **kwargs):
    """PushPlus消息推送"""
    pushplus_url = "https://www.pushplus.plus/send"
    token = meta.get('host', '')
    response = requests.post(
        pushplus_url,
        json={
            "token": token,
            "title": title,
            "content": body
        },
        headers={'Content-Type': 'application/json'},
        timeout=10
    )
    response.raise_for_status()
    logger.info("✅ PushPlus响应: %s", response.text)
